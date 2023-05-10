import argparse
import sys
from threading import Semaphore, Thread
import threading

PARSER = argparse.ArgumentParser()
PARSER.add_argument("input_string", help="Cadena de entrada")
LETTERS_NUMBERS = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5',
                   'F': '6', 'G': '7', 'H': '8', 'I': '9', 'J': '10',
                   'K': '11', 'L': '12', 'M': '13', 'N': '14', 'O': '15',
                   'P': '16', 'Q': '17', 'R': '18', 'S': '19', 'T': '20',
                   'U': '21', 'V': '22', 'W': '23', 'X': '24', 'Y': '25',
                   'Z': '26'}
CHARS_STATE = []
RESULT_LIST = []
MUTEX = Semaphore(1)

def get_input_string():
    """
    Obtiene la cadena de entrada desde los argumentos.

    Returns:
        string, la cadena de entrada.
    """
    args = PARSER.parse_args()
    input_string = args.input_string
    input_string = input_string.upper()
    if not input_string.isalpha():
        print("La cadena solo puede contener caracteres alfabéticos. ")
        print("Por ejemplo: Hola")
        sys.exit(1)
    return input_string

def is_char_available(pos):
    """
    Informa si un caracter está disponible para procesar.

    Returns:
        boolean, el estado del caracter: True = disponible
        False = ocupado.
    """
    return CHARS_STATE[pos]

def set_char_as_unavailable(pos):
    """
    Setea el caracter como ocupado en el vector de estados.
    """
    CHARS_STATE[pos] = False

def process_char(input_string, index):
    """
    Procesa la letra y guarda el número correspondiente
    en la posición correspondiente de la lista resultado.
    """
    RESULT_LIST[index] = LETTERS_NUMBERS[input_string[index]]

def thread_job(input_string, num_chars_to_process):
    """
    Es la función que realizará el trabajo del thread.
    Es decir, procesará la cantidad de caracteres indicados
    como parámetros.
    """
    num_processed_chars = 0
    # Mientras no haya procesado la cantidad de caracteres
    # que recibe como parámetro, sigue buscando candidatos
    while num_processed_chars < num_chars_to_process:
        # Recorro todos los caracteres de la cadena en busca
        # de candidatos a procesar
        for i in range(len(input_string)):
            char_available = False
            # Uso el mutex para verificar si el caracter actual
            # está disponible para procesar
            MUTEX.acquire()
            char_available = is_char_available(i)
            # Si el caracter está disponible, lo voy a tomar. Así
            # que lo marco como ocupado y libero el mutex
            if(char_available):
                set_char_as_unavailable(i)
            else:
                print("\t")
            MUTEX.release()
            # Si pude tomar el caracter, lo proceso y sumo el contador
            # de caracteres procesados. De lo contrario, sigo buscando
            # un caracter candidato
            if(char_available):
                process_char(input_string, i)
                num_processed_chars += 1
            if(num_processed_chars == num_chars_to_process):
                break




    

def main():
    input_string = get_input_string()

    # Inicializo un vector de booleanos cuyo valor
    # de cada posición indica si ese caracter de la
    # cadena fue procesado o se tomó para procesar
    global CHARS_STATE
    CHARS_STATE = [True] * len(input_string)

    # Inicializo la lista resultante de números
    global RESULT_LIST
    RESULT_LIST = [""] * len(input_string)

    # Defino la cantidad de caracteres a procesar para
    # cada hilo
    num_chars_to_process_t1 = len(input_string) // 2
    num_chars_to_process_t2 = len(input_string) - num_chars_to_process_t1

    first_thread = Thread(target=thread_job, args=(input_string, num_chars_to_process_t1))
    second_thread = Thread(target=thread_job, args=(input_string, num_chars_to_process_t2))

    first_thread.start()
    second_thread.start()

    first_thread.join()
    second_thread.join()

    print("Lista resultado: ", RESULT_LIST)


main()