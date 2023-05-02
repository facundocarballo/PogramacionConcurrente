#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

#include <iostream>

#define FIFO_PERMISSIONS 0666
#define POS_NUMBERS 1
#define STR_INITIAL_POS 0
#define STR_NEXT_POS 1
#define CHAR_SEPARATOR '-'

typedef struct t_info 
{
  float average;
  int max, min, addition, amount;
} Info;

int fileA, fileB, num, amount = 1;
const char* kFifoA = "/tmp/TP3_M3-A";
const char* kFifoB = "/tmp/TP3_M3-B";
Info info;

void SendAmountOfNumbers(std::string msg);
void SendNumbers(std::string msg);
void PrintInfo(Info* info);
void Help();

int main(int argc, char* argv[]) 
{
  if (argc != 2)
  {
    Help();
    return EXIT_FAILURE;
  }

  fileA = open(kFifoA, O_WRONLY);
  fileB = open(kFifoB, O_RDONLY);

  // Send data
  SendAmountOfNumbers(argv[POS_NUMBERS]);
  SendNumbers(argv[POS_NUMBERS]);

  // Receive data.
  read(fileB, &info, sizeof(Info));

  PrintInfo(&info);

  close(fileB);
  close(fileA);
}

void SendNumbers(std::string msg) 
{
  int pos = msg.find(CHAR_SEPARATOR);
  while (pos != std::string::npos) 
  {
    num = stoi(msg.substr(STR_INITIAL_POS, pos));
    write(fileA, &num, sizeof(int));
    msg = msg.substr(pos + STR_NEXT_POS);
    pos = msg.find(CHAR_SEPARATOR);
  }
  num = stoi(msg);
  write(fileA, &num, sizeof(int));
}

void SendAmountOfNumbers(std::string msg) 
{
  int pos = msg.find(CHAR_SEPARATOR);
  while (pos != std::string::npos) 
  {
    amount++;
    msg = msg.substr(pos + STR_NEXT_POS);
    pos = msg.find(CHAR_SEPARATOR);
  }
  write(fileA, &amount, sizeof(int));
}

void PrintInfo(Info* info) 
{
  std::cout << "Promedio: " << info->average << std::endl;
  std::cout << "Mínimo: " << info->min << std::endl;
  std::cout << "Máximo: " << info->max << std::endl;
  std::cout << "Suma: " << info->addition << std::endl;
  std::cout << "Cantidad: " << info->amount << std::endl;
}

void Help()
{
    std::cout << "Este programa envia una secuencia de numeros a un servidor y espera esta informacion:" << std::endl;
    std::cout << "  - Promedio" << std::endl;
    std::cout << "  - Mínimo" << std::endl;
    std::cout << "  - Máximo" << std::endl;
    std::cout << "  - Suma" << std::endl;
    std::cout << "  - Cantidad" << std::endl;
    std::cout << "Como ejecutar el programa correctamente?" << std::endl;
    std::cout << "./client 1-2-3-4" << std::endl;
    std::cout << "Siendo 1-2-3-4 mi secuencia de numeros de la cual yo quiero obtener informacion." << std::endl;
}