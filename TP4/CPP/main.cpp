#include <iostream>
#include <mutex>
#include <thread>

#define INIT_POS 0
#define MAX_POS 10
#define MIDDLE_POS (MAX_POS / 2)

// Global Variables
int arr[MAX_POS] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
int suma_total;
std::mutex mtx;

void Suma(int i, int max) 
{
  for (i; i < max; i++) 
  {
    mtx.lock();
    suma_total += arr[i];
    mtx.unlock();
  }
}

int main() 
{
  std::thread hilo_a(Suma, INIT_POS, MIDDLE_POS);
  std::thread hilo_b(Suma, MIDDLE_POS, MAX_POS);

  hilo_a.join();
  hilo_b.join();
  
  std::cout << "Suma Total: " << suma_total << std::endl;

  return EXIT_SUCCESS;
}