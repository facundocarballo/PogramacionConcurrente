"""
Uso de PIPES
"""

import argparse
from multiprocessing import Pipe
import os
import signal
import sys

BYTES_PER_CHUNK = 512
PARSER = argparse.ArgumentParser()
PARSER.add_argument("filedir", help="El directorio del archivo a copiar")
# Puse un enter aca para que la linea no sea tan larga
# no pude poner el parentesis abajo porque tira error
PARSER.add_argument(
    "bytes_per_chunk",
    nargs="?",
    default=512,
    help="La cantidad de bytes a transferir por chunk"
)

def is_text_file(file):
    """
    Devuelve si un archivo es de texto o no, comparando
    la extensión.

    Args:
        file: string, el directorio del archivo.

    Returns:
        boolean, el archivo es o no de texto.
    """
    # Esta función retorna una tupla en la que están
    # el path del archivo y su extensión
    _, extension = os.path.splitext(file)
    extension = extension.lower()
    # Si extension se encuentra en la tupla, retornará True,
    # de lo contrario, retornará False. Si queremos evaluar
    # otras extensiones, bastará con agregarlas a la tupla.
    return extension in [".txt"]

def get_filedir():
    """
    Obtiene el directorio del archivo a copiar desde los argumentos

    Returns:
        string, el directorio del archivo.
    """
    args = PARSER.parse_args()
    filedir = args.filedir
    if not is_text_file(filedir):
        print("El archivo debe ser un archivo de texto. ")
        print("Por ejemplo: file.txt")
        sys.exit(1)
    return filedir

def set_bytes_per_chunk():
    """
    Configura la cantidad a bytes a transferir por chunk
    desde los argumentos.
    """
    args = PARSER.parse_args()
    global BYTES_PER_CHUNK
    BYTES_PER_CHUNK = int(args.bytes_per_chunk)

def get_copy_file_name(filedir):
    """
    Obtiene el directorio de la copia del archivo.
    El nombre del archivo copia tiene que ser el nombre
    del archivo original, concatenado con "_copia" al final.

    Args:
        filedir: string, el directorio del archivo original.

    Returns:
        string, el directorio de la copia del archivo.
    """
    path, extension = os.path.splitext(filedir)
    extension = extension.lower()
    return path + "_copia" + extension

def send_file(sender, receiver, filedir):
    """
    Envía el contenido del archivo original por el pipe.

    Args:
        sender: objeto Pipe, el extremo del pipe por el que se envía el contenido del archivo.
        receiver: objeto Pipe, el extremo del pipe por el que se recibe el contenido del archivo.
        filedir: string, el directorio del archivo original.
    """
    receiver.close()
    with open(filedir, "r", encoding="utf-8") as original_file:
        data = original_file.read(BYTES_PER_CHUNK)
        while data:
            sender.send_bytes(data.encode("utf-8"))
            data = original_file.read(BYTES_PER_CHUNK)
    original_file.close()
    sender.close()

def copy_file(sender, receiver, copy_filedir):
    """
    Recibe el contenido del archivo original por el pipe y lo copia
    en un archivo nuevo.

    Args:
        sender: objeto Pipe, el extremo del pipe por el que se envío el contenido del archivo.
        receiver: objeto Pipe, el extremo del pipe por el que se recibe el contenido del archivo.
        copy_filedir: string, el directorio del archivo copia.
    """
    sender.close()
    try:
        with open(copy_filedir, "w", encoding="utf-8") as copied_file:
            try:
                data = receiver.recv_bytes(BYTES_PER_CHUNK).decode("utf-8")
                while data:
                    copied_file.write(data)
                    print("Copiando ", len(data), " bytes")
                    data = receiver.recv_bytes(BYTES_PER_CHUNK).decode("utf-8")
            except EOFError:
                pass
            print("El archivo se copió exitosamente.")
    except(FileNotFoundError, PermissionError):
        print("No se puede crear o escribir el archivo copia.")

    copied_file.close()
    receiver.close()

def main():
    filedir = get_filedir()

    # Me fijo si el archivo existe y si se puede abrir
    try:
        with open(filedir, "r", encoding="utf-8"):
            pass
    except(FileNotFoundError, PermissionError, IOError):
        print("El archivo no existe o no se puede abrir. Finalizando.")
        sys.exit(1)

    copy_filedir = get_copy_file_name(filedir)
    set_bytes_per_chunk()

    receiving, sending = Pipe(False)

    pid = os.fork()
    if pid < 0:
        print("Error al crear el nuevo proceso")
        sys.exit(1)

    if pid:
        send_file(sending, receiving, filedir)
        os.wait()
    else:
        copy_file(sending, receiving, copy_filedir)
        sys.exit(0)


main()