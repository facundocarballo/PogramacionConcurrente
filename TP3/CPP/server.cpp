#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

#include <iostream>

#define FIFO_PERMISSIONS 0666
#define MKFIFO_ERROR -1
#define INFO_MAX_INIT_VALUE 0
#define INFO_MIN_INIT_VALUE 2147483647
#define INFO_AVERAGE_INIT_VALUE 0
#define INFO_ADITION_INIT_VALUE 0

typedef struct t_info 
{
  float average;
  int max, min, addition, amount;
} Info;

void InitInfo(Info*, int*);
bool TryChangeMax(Info*, int*);
bool TryChangeMin(Info*, int*);
void IncrementAddition(Info*, int*);
void SetAverage(Info*);
void MakeDeamon();

int fileA, fileB, num;
const char* kFifoA = "/tmp/TP3_M3-A";
const char* kFifoB = "/tmp/TP3_M3-B";
Info info;

int main() 
{
  MakeDeamon();

  if (mkfifo(kFifoB, FIFO_PERMISSIONS) == MKFIFO_ERROR) 
  {
    perror("Error al crear el FIFO.");
    return EXIT_FAILURE;
  }

  if (mkfifo(kFifoA, FIFO_PERMISSIONS) == MKFIFO_ERROR) 
  {
    perror("Error al crear el FIFO.");
    return EXIT_FAILURE;
  }

  fileA = open(kFifoA, O_RDONLY);
  fileB = open(kFifoB, O_WRONLY);

  read(fileA, &num, sizeof(int));
  InitInfo(&info, &num);
  for (int i = 0; i < info.amount; i++) 
  {
    read(fileA, &num, sizeof(int));
    TryChangeMax(&info, &num);
    TryChangeMin(&info, &num);
    IncrementAddition(&info, &num);
  }
  SetAverage(&info);
  write(fileB, &info, sizeof(Info));

  close(fileA);
  close(fileB);
  unlink(kFifoB);
  unlink(kFifoA);

  return EXIT_SUCCESS;
}

void MakeDeamon()
{
  int pid = fork();
  if (pid < 0)
  {
    perror("Fork error.");
  }
  else if (pid > 0)
  {
    exit(EXIT_SUCCESS);
  }
}

void InitInfo(Info* info, int* amount) 
{
  info->addition = INFO_ADITION_INIT_VALUE;
  info->amount = *amount;
  info->average = INFO_AVERAGE_INIT_VALUE;
  info->max = INFO_MAX_INIT_VALUE;
  info->min = INFO_MIN_INIT_VALUE;
}

bool TryChangeMax(Info* info, int* num) 
{
  if (*num > info->max) {
    info->max = *num;
    return true;
  }

  return false;
}

bool TryChangeMin(Info* info, int* num) 
{
  if (*num < info->min) {
    info->min = *num;
    return true;
  }

  return false;
}

void IncrementAddition(Info* info, int* num) 
{ 
    info->addition += *num; 
}

void SetAverage(Info* info) 
{
  info->average = (float)info->addition / (float)info->amount;
}