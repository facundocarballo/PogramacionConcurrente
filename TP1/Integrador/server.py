from Crypto.Cipher import AES
from pathlib import Path
import threading
import os
import sys
import pickle
import signal
import errno
import time

# Bytes
BYTES_16 = 16
BYTES_1024 = 1024

# FIFOs
FIFO_A_PATH = "/tmp/FIFO_A"
FIFO_B_PATH = "/tmp/FIFO_B"
FIFO_A = None
FIFO_B = None
FIFO_PERMISSIONS = 0o600

# Args
ARGV_1 = 1
ARGV_2 = 2
ARGV_3 = 3
ARGV_AMOUNT = 4
ARG_ENCRYPT = "-e"
ARG_DECRYPT = "-d"

# File
FILE_READ_BYTE = "rb"
FILE_READ_TEXT = "r"
FILE_APPEND = "a"
FILE_WRITE_TEXT = "w"
FILE_WRITE_BYTE = "wb"
FILE_START_WITH = "File("
FILE_END_WITH = ")"
FILE_FIND_ERROR = -1

# String
EMPTY_STRING = ""
SPACES_2 = "  "

# Hexa
HEX_START_WITH = "0x"

# Cipher
CIPHER_PATH = './cipher.enc'
IV_KEY = "Concurrencia!!!!".encode('utf-8').ljust(BYTES_16, b'\0')

# Mutex
mutex = threading.Lock()
mutex_folder = threading.Lock()

# Threads
threads = []

# Global Variables
module = None
file_path = None
key = None
obj = None

class Info:
    def __init__(self, module, path, key):
        self.module = module
        self.path = path
        self.key = key

# Signal Managment
def close_server(signal, frame):
    """
    @params:
        [signal]: Is the number of the signal that the process receives.
        [frame]: Information about the stack trace of the process.
    
    @description:
        This function handles the ending of the server.
        Closing all the resources that the Server used.
    """

    # Mark global variables 
    global FIFO_A
    global FIFO_B

    print("Closing server")

    # Close the FIFOs
    if FIFO_A != None:
        os.close(FIFO_A)

    if FIFO_B != None:
        os.close(FIFO_B)

    # Unlink the FIFOs
    os.unlink(FIFO_A_PATH)
    os.unlink(FIFO_B_PATH)

    sys.exit(0)

signal.signal(signal.SIGUSR1, close_server)
signal.signal(signal.SIGINT, close_server)

# Encrypt and Decrypt Functions
def encrypt_file(key, path, spaces):
    """
    @params:
        key: Is the key that this function use to encript the file.
        path: Is the path to the file that this function will encript.
        spaces: Is the amount of spaces that this function needs to print on the cypher.enc file.
    """
    # Create a cipher obj with AES Algorithm
    cipher = AES.new(key.encode('utf-8', 'ignore'), AES.MODE_CBC, IV_KEY)
    
    # Read the entire file in bytes
    with open(path, FILE_READ_BYTE) as f:
        plaintext = f.read()

    # Add some padding to make it multiple of 16 bytes
    plaintext += b"\0" * (AES.block_size - len(plaintext) % AES.block_size)

    # Cipher the archive using AES on CBC mode
    ciphertext = cipher.encrypt(plaintext)

    # Write in the cipher.enc file the ciphertext with a reference to the original file
    with open(CIPHER_PATH, FILE_APPEND) as f:
        write(spaces + "  File(" + path + ") -> 0x" + str(ciphertext.hex()) + "\n", f)

    # Delete the uncipher file
    os.remove(path)

def encrypt_folder(key, directory, spaces):
    """
    @params:
        key: Is the key that this function use to encript the file.
        directory: Is the directory that this function will encript.
        spaces: Is the amount of spaces that this function needs to print on the cypher.enc file.
    
    @description:
        This function will encript all the files that are include in this folder.
        If this folder contains a sub folder, this function will call himself recursively
        to encript that subfolder too.
    """

    # Request fot the mutext_folder to write the encript file propertly.
    mutex_folder.acquire()

    # Open the encript file and print the name of the folder.
    with open(CIPHER_PATH, FILE_APPEND) as f:
        write(spaces + "Folder (" + str(directory) + ")" + "\n", f)

    # Loop all the files into this folder to encript them.
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if os.path.isdir(path):
            # If the path is a directory creates a thread to loop that folder and encript the files.
            thread = threading.Thread(
                target=encrypt_folder,
                args=(key, path, spaces + SPACES_2)
            )
            thread.start()
            # Add that thread to our threads array to then join them.
            threads.append(thread)
        else:
            # If the path is a file, just encript the file.
            encrypt_file(key, path, spaces)
    
    # Release the mutex folder for others threads.
    mutex_folder.release()

def decrypt_file(key, ciphertext):
    """
    @params:
        key: Is the key that this function will use to decript the file.
        ciphertext: Is the hex code generetes on the encript file, but in bytes!!!
    """
    cipher = AES.new(key.encode('utf-8', 'ignore'), AES.MODE_CBC, IV_KEY)
    descipher_text = cipher.decrypt(ciphertext)

    return descipher_text.decode('utf-8', 'ignore')

# Write and Read functions
def write(msg, f):
    """
    @params:
        msg: Is the message that this function will write.
        f: Is the file that this function will write.
    """

    # Request the mutext to write the file propertly.
    mutex.acquire()

    f.write(msg)
    
    # Release the mutext.
    mutex.release()

def read_cipher_file(path, key):
    """
    @params:
        path: Is the path of the encripted file.
        key: Is the key to decript the file.

    @description:
        This function will read the encripted file line by line looking for encripted files.
        If the encripted file contains encripted files, would get for those:
            - Director: Directory of that encripted file.
            - Ciphertext: Hex code associate to this file.
            - Plaintext: Plaintext of this encripted file.
        Then, this function will write in the corresponding file, the corresponding plain text
        of the file that was encripted.
    """

    # Open the encripted file
    with open(path, FILE_READ_TEXT) as file:
        # Loop line by line looking for encripted files into it.
        for line in file:
            if (line.find(HEX_START_WITH) != FILE_FIND_ERROR):
                # Get the data of this encripted file
                directory = get_directory(line)
                ciphertext = get_ciphertext(line)
                plaintext = decrypt_file(key, ciphertext)

                # Open the uncripted file to write in it the plaintext
                with open(directory, FILE_WRITE_TEXT) as new_file:
                    new_file.write(plaintext)

# Helpers
def get_directory(line):
    """
    @params:
        line: String that contains the directory.
    """

    spaces = str(line).find(FILE_START_WITH)
    directory_start = len(FILE_START_WITH) + spaces
    directory_end = str(line).find(FILE_END_WITH)
    directory = str(line)[directory_start:directory_end]

    return directory

def get_ciphertext(line):
    """
    @params:
        line: String that contains the ciphertext.
    """

    spaces = str(line).find(HEX_START_WITH)
    directory_start = len(HEX_START_WITH) + spaces
    ciphertext = str(line)[directory_start:len(line)]
    bytes_hex = bytes.fromhex(ciphertext)
    return bytes_hex

def check_obj():
    """
    @description:
        This function verify the object readed on the fifo.
        Have to guaranteed that the object applies correctly our structure, otherwise will responde to the client with an error.
    """
    global obj
    
    if obj == None:
        return
    
    path = Path(obj.path)

    # Check real path
    if path.exists() == False:
        fifo_write("The path doesn't exist.")
        return
    
    # Check decrypt
    if obj.module == ARG_DECRYPT:
        if path.is_file() == False:
            fifo_write("To decrypt you have to send a cipher file.")
            return
        
        main_decrypt()
        fifo_write("Decryption done.")
        return
    
    # Check encrypt
    if obj.module == ARG_ENCRYPT:
        if path.is_dir() == False:
            fifo_write("To encrypt you have to send a folder.")
            return
            
        main_encrypt()
        fifo_write("Encryption done.")
        return

# Main functions
def main_encrypt():
    """
    @description:
      This is the main function that handle the files encryption.
    """
    global obj

    # Get the path from the argument.
    path = obj.path

    # Create a 16 bytes key with the key argument.
    key = obj.key.ljust(BYTES_16)[:BYTES_16]

    # Create a Path obj
    directory = Path(path)

    encrypt_folder(key, directory, EMPTY_STRING)
    
    # Join all the threads that were created.
    for thread in threads:
        thread.join()

def main_decrypt():
    """
    @description:
      This is the main function that handles the files decryption.
    """
    # Generate a 16 bytes key
    key = obj.key.ljust(BYTES_16)[:BYTES_16]

    # Get a Path
    directory = Path(obj.path)

    read_cipher_file(directory, key)

    # Delete the cipher file.
    os.remove(CIPHER_PATH)

# FIFOs Functions
def fifo_creates():
    """
    @description:
      This function only try to create the FIFOs to use.
    """
    try:
        os.mkfifo(FIFO_A_PATH, FIFO_PERMISSIONS)
    except OSError as error:
        print("Error creating the FIFO_A: ", error)
    
    try:
        os.mkfifo(FIFO_B_PATH, FIFO_PERMISSIONS)
    except OSError as error:
        print("Error creating the FIFO_B: ", error)
    
def fifos_open():
    """
    @description:
      This function only tries to open the FIFOs.
    """

    # Mark the global variables.
    global FIFO_A 
    global FIFO_B

    try:
        FIFO_A = os.open(FIFO_A_PATH, os.O_RDONLY)
    except OSError as error:
        print("Error opening the FIFO_A: ", error)

    # Is blocked until the client opens his file in READ ONLY
    try:
        FIFO_B = os.open(FIFO_B_PATH, os.O_WRONLY)
    except OSError as error:
        print("Error opening the FIFO_B: ", error)

def fifo_read():
    """
    @description:
      This function only reads the FIFO_A where the client is putting his request.
    """

    # Mark the global variables.
    global obj

    data = os.read(FIFO_A, BYTES_1024)
    if data:
        obj = pickle.loads(data)

def fifo_write(msg):
    """
    @params:
      - [msg]: Is the message that will be writed on the FIFO_B
    
    @description:
      This function only writes a message on the FIFO_B
    """
    
    os.write(FIFO_B, str(msg).encode('utf-8', 'ignore'))

# Main Function
def main():
    """
    @description:
      This is the Server main function.
    """
    
    # Mark global variables
    global obj
    global FIFO_B
    global FIFO_A

    print("Server running with PID: ", os.getpid())

    fifo_creates()
    fifos_open()

    while True:
        # Clear the Object
        obj = None
        
        # Read the FIFO_A
        try:
            fifo_read()
        except OSError as error:
            if error.errno == errno.EAGAIN or error.errno == errno.EWOULDBLOCK:
                # There is not data on FIFO_A
                time.sleep(1)
                continue
            else:
                print("Error reading from FIFO_A: ", error)
                break

        check_obj()

main()