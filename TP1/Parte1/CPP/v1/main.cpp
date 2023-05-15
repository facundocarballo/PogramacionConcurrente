#include <iostream>
#include <unistd.h>
#include <sys/wait.h>

using namespace std;

void print_process_message(char char_of_process)
{
    cout << "Proceso " << char_of_process << " ( PID: " << getpid() << " | PPID: " << getppid() << " )" << endl;
}

int main(int argc, char *argv[])
{
    pid_t pidA, pidB, pidC, pidD, pidE, pidF, pidG;
    pidA = getpid();
    print_process_message('A');
    pidB = fork();
    if (pidB == 0)
    {
        pidB = getpid();
        print_process_message('B');
        pidE = fork();
        if (pidE == 0)
        {
            pidE = getpid();
            print_process_message('E');
            sleep(30);
            exit(0);
        }
        pidF = fork();
        if (pidF == 0)
        {
            pidF = getpid();
            print_process_message('F');
            sleep(30);
            exit(0);
        }
        sleep(30);
        wait(NULL);
        wait(NULL);
        exit(0);
    }
    pidC = fork();
    if (pidC == 0)
    {
        pidC = getpid();
        print_process_message('C');
        sleep(30);
        exit(0);
    }
    pidD = fork();
    if (pidD == 0)
    {
        pidD = getpid();
        print_process_message('D');
        pidG = fork();
        if (pidG == 0)
        {
            pidG = getpid();
            print_process_message('G');
            sleep(30);
            exit(0);
        }
        sleep(30);
        wait(NULL);
        exit(0);
    }
    sleep(30);
    wait(NULL);
    wait(NULL);
    wait(NULL);
    return 0;
}