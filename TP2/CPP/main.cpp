#include <chrono>
#include <iostream>
#include <string>
#include <thread>
#include <tuple>
#include <vector>

#define CANTIDAD_NUMEROS 65
#define LIMITE 32

#define ORDEN_MAXIMO 20
#define ORDEN_MINIMO 5

#define MATRIZ_A "A"
#define MATRIZ_B "B"
#define MATRIZ_SECUENCIAL "CS"
#define MATRIZ_HILOS "CH"

void Ayuda() 
{
  printf(
      "Enviar un parametro indicando la cantidad de filas y columnas de la "
      "matriz.\n");
  printf("------\n");
  printf("Ejemplo:\n");
  printf("./matrix 3\n");
  printf("------\n");
  printf("Esto hara que el programa trabaje con una matrix de 3x3\n");
  printf("------\n");
  printf("Los ordenes de matriz aceptados van desde %d hasta %d.\n", ORDEN_MINIMO, ORDEN_MAXIMO);
}

class Matriz 
{
 private:
  int orden_;
  int** matriz_;
  std::string nombre_;

  void ImprimirConEstilo(int n) 
  {
    if (n > 99) 
    {
      std::cout << " " << n << "  ";
    } else if (n > 9) 
    {
      std::cout << "  " << n << "  ";
    } else if (n > 0) 
    {
        std::cout << "   " << n << "  ";
    }
    else if (n > -10) 
    {
      std::cout << "  " << n << "  ";
    } else if (n > -100) 
    {
      std::cout << " " << n << "  ";
    } else 
    {
        std::cout << n << "  ";
    }
  }
  void MultiplicarFila(int fila, Matriz* B, Matriz* C) 
  {
    for (int i = 0; i < this->orden_; i++) 
    {
      C->matriz_[fila][i] = this->matriz_[fila][i] * B->matriz_[fila][i];
    }
  }

 public:
  Matriz(int orden, std::string nombre) 
  {
    this->orden_ = orden;
    this->nombre_ = nombre;
    matriz_ = new int*[orden];
    for (int i = 0; i < orden; i++) 
    {
      matriz_[i] = new int[orden];
    }
  }
  void Random() 
  {
    for (int i = 0; i < this->orden_; i++) 
    {
      for (int j = 0; j < this->orden_; j++) 
      {
        matriz_[i][j] = rand() % CANTIDAD_NUMEROS + (-LIMITE);
      }
    }
  }
  void Imprimir() 
  {
    std::cout << "Matriz: " << this->nombre_ << std::endl;
    for (int i = 0; i < this->orden_; i++) 
    {
      for (int j = 0; j < this->orden_; j++) 
      {
        this->ImprimirConEstilo(this->matriz_[i][j]);
      }

      std::cout << std::endl;
    }
  }
  std::tuple<Matriz*, std::chrono::_V2::system_clock::duration>
  Multiplicar(Matriz* B) 
  {
    Matriz* C = new Matriz(this->orden_, MATRIZ_SECUENCIAL);
    auto comienzo = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < this->orden_; i++) 
    {
      for (int j = 0; j < this->orden_; j++) 
      {
        C->matriz_[i][j] = this->matriz_[i][j] * B->matriz_[i][j];
      }
    }
    auto fin = std::chrono::high_resolution_clock::now();
    return std::make_tuple(C, fin - comienzo);
  }
  std::tuple<Matriz*, std::chrono::_V2::system_clock::duration>
  MultiplicarConcurrente(Matriz* B) 
  {
    Matriz* C = new Matriz(this->orden_, MATRIZ_HILOS);
    std::vector<std::thread> hilos;
    auto comienzo = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < this->orden_; i++) 
    {
      hilos.emplace_back(&Matriz::MultiplicarFila, this, i, B, C);
    }

    for (auto& h : hilos) 
    {
      h.join();
    }

    auto fin = std::chrono::high_resolution_clock::now();

    return std::make_tuple(C, fin - comienzo);
  }
  bool EsIgualA(Matriz* B)
  {
    bool res = true;
    int i = 0;
    int j = 0;
    while(res && i < this->orden_)
    {
      while(res && j < this->orden_)
      {
        if (this->matriz_[i][j] != B->matriz_[i][j])
        {
          res = false;
        }
        j++;
      }
      i++;
    }
    return res;
  }
};

void ImprimirTiempo(std::chrono::milliseconds tiempo) 
{
  std::cout << "Hecho en: " << tiempo.count() << " ms" << std::endl;
}

Matriz* MultiplicacionSecuencial(Matriz* A, Matriz* B) 
{
  std::cout << "\nMultiplicacion Secuencial" << std::endl;
  Matriz* C;
  std::chrono::_V2::system_clock::duration tiempo;
  std::tie(C, tiempo) = A->Multiplicar(B);
  C->Imprimir();
  ImprimirTiempo(std::chrono::duration_cast<std::chrono::milliseconds>(tiempo));

  return C;
}

Matriz* MultiplicacionConcurrente(Matriz* A, Matriz* B) 
{
  std::cout << "\nMultiplicacion Concurrente" << std::endl;
  Matriz* D;
  std::chrono::_V2::system_clock::duration tiempo2;
  std::tie(D, tiempo2) = A->MultiplicarConcurrente(B);
  D->Imprimir();
  ImprimirTiempo(
      std::chrono::duration_cast<std::chrono::milliseconds>(tiempo2));

  return D;
}

int main(int argc, char* argv[]) 
{
  if (argc != 2) 
  {
    Ayuda();
    return EXIT_FAILURE;
  }

  int n = std::stoi(argv[1]);

  if (n < ORDEN_MINIMO || n > ORDEN_MAXIMO)
  {
    Ayuda();
    return EXIT_FAILURE;
  }

  Matriz* A = new Matriz(n, MATRIZ_A);
  A->Random();
  A->Imprimir();

  Matriz* B = new Matriz(n, MATRIZ_B);
  B->Random();
  B->Imprimir();

  Matriz* C = MultiplicacionSecuencial(A, B);
  Matriz* D = MultiplicacionConcurrente(A, B);

  if (C->EsIgualA(D))
  {
    std::cout << "Las matrices son iguales." << std::endl;
  }
  else
  {
    std::cout << "Las matrices son diferentes." << std::endl;
  }

  return EXIT_SUCCESS;
}