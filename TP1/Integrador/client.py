import os
import sys
import pickle

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

class Info:
    def __init__(self, module, path, key):
        self.module = module
        self.path = path
        self.key = key

def help():
    """
    @description:
      This is the Client help function.
    """
    print("HELP")
    print("---------------------------------")
    print("Example of how to execute this program.")
    print("  python3 ./client [module] [path] [key]")
    print("    - [module]:")
    print("      '-e': Encrypting")
    print("      '-d': Decrypting")
    print("    - [path]: Is the path of the folder or file to encrypt or decrypt.")
    print("    - [key]: Is the key to encrypt or decrypt the files.")
    print("---------------------------------")

def main():
    """
    @description:
      This is the Client main function.
    """

    # Check arguments
    if len(sys.argv) != ARGV_AMOUNT:
        help()
        sys.exit(1)

    # Get the module that we want to use (encrypt or decrypt)
    module = sys.argv[ARGV_1]

    # Check the module send by the user
    if module != ARG_DECRYPT and module != ARG_ENCRYPT:
        help()
        sys.exit(1)

    # Get the path from the argument.
    path = sys.argv[ARGV_2]

    # Create a 16 bytes key with the key argument.
    key = sys.argv[ARGV_3].ljust(BYTES_16)[:BYTES_16]

    # Try to open the FIFOs
    try:
        FIFO_A = os.open(FIFO_A_PATH, os.O_WRONLY | os.O_NONBLOCK)
    except OSError as error:
        print("Error opening the FIFO_A: ", error)
        return
    
    try:
        FIFO_B = os.open(FIFO_B_PATH, os.O_RDONLY)
    except OSError as error:
        print("Error opening the FIFO_B: ", error)
        return
    
    obj = Info(module, path, key)

    # Convert the obj to bytes
    obj_bytes = pickle.dumps(obj)

    # Write the obj on the FIFO_A
    os.write(FIFO_A, obj_bytes)

    # aqui

    # Wait for server response
    status = os.read(FIFO_B, BYTES_1024)

    print("Server response: \n  -> " + status.decode('utf-8', 'ignore'))

    # Close FIFOs
    os.close(FIFO_A)
    os.close(FIFO_B)

main()