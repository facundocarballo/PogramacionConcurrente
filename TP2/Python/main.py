import random
import threading
import time 

#########################Declaraciones#############################
global A, B
N = 5
A = [[random.randint(-32, 32) for _ in range(N)] for _ in range(N)]
B = [[random.randint(-32, 32) for _ in range(N)] for _ in range(N)]
CS = [[0 for _ in range(N)] for _ in range(N)]
CH = [[0 for _ in range(N)] for _ in range(N)]
####################################################################

#########################Multiplicaciones###########################
def multiplicar_matrices_secuenciales(N):
  for i in range(N):
    for j in range(N):
      for k in range(N):
        CS[i][j] += A[i][k] * B[k][j]

  return CS


def multiplicar_matrices_con_hilos(N):
  def multiplicar_fila_hilo(fila):
    for j in range(N):
      for k in range(N):
        CH[fila][j] += A[fila][k] * B[k][j]

  hilos = []
  for i in range(N):
    hilo = threading.Thread(target=multiplicar_fila_hilo, args=(i,))
    hilos.append(hilo)
    hilo.start()

  for hilo in hilos:
    hilo.join()

  return CH
####################################################################

#########################Evaluadores################################

def comparar_matrices(A, B):
  res = True
  for i in range(N):
    for j in range(N):
      if (A[i][j] != B[i][j]):
        res = False
        break
  return res


############################Ejecuciones#############################

inicio_secuencial = time.time() # registra el tiempo de inicio
resultado_CS = multiplicar_matrices_secuenciales(N)
fin_secuencial = time.time() # registra el tiempo de finalización

inicio_hilo = time.time() # registra el tiempo de inicio
resultado_CH = multiplicar_matrices_con_hilos(N)
fin_hilo = time.time() # registra el tiempo de finalización

tiempo_total_secuencial = fin_secuencial - inicio_secuencial # calcula el tiempo total de ejecución
tiempo_total_hilo = fin_hilo - inicio_hilo # calcula el tiempo total de ejecución
print("\n")
print(f"La función secuencial tardó {tiempo_total_secuencial} segundos en ejecutarse.")
print(f"La función hilo tardó {tiempo_total_hilo} segundos en ejecutarse.")
print("\n")

###################################################################

############################Impresiones#############################
print("Matriz A:")
for fila in A:
  print(fila)
print("\nMatriz B:")
for fila in B:
  print(fila)
print("\nMatriz CH:")
for fila in resultado_CH:
  print(fila)
print("\nMatriz CS:")
for fila in resultado_CS:
  print(fila)

if (comparar_matrices(resultado_CS, resultado_CH)):
  print("\nLas matrices son iguales.")
else:
  print("\nLas matrices son diferentes.")

###################################################################