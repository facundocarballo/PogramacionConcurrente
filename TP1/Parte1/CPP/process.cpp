#include <sys/wait.h>
#include <unistd.h>
#include <iostream>
#include <list>

#define TIME_SLEEP 30
#define PROCESS_A "A"
#define PROCESS_B "B"
#define PROCESS_C "C"
#define PROCESS_D "D"
#define PROCESS_E "E"
#define PROCESS_F "F"
#define PROCESS_G "G"

class ProcessBase 
{
 public:
  ProcessBase(){};
  virtual void Execute() = 0;
  void PrintMessage(std::string name) 
  {
    std::cout << "Proceso " + name + " ( PID: " + std::to_string(getpid()) +
                     " | PPID: " + std::to_string(getppid()) + " )"
              << std::endl;
  }
  void PrintErrorMessage(std::string name)
  {
    std:: cout << "Error al crear el proceso " + name + "." << std::endl;
  }
};

class ProcessLead : public ProcessBase 
{
 private:
  std::string name_;

 public:
  ProcessLead(std::string name) { this->name_ = name; }
  void Execute() override 
  {
    this->PrintMessage(this->name_);
    sleep(TIME_SLEEP);
    exit(EXIT_SUCCESS);
  }
};

class ProcessParent : public ProcessBase 
{
 private:
  std::string name_;
  std::list<ProcessBase*> childs_;

 public:
  ProcessParent(std::string name, std::list<ProcessBase*> childs) 
  {
    this->name_ = name;
    this->childs_ = childs;
  }

  void Execute() 
  {
    this->PrintMessage(this->name_);
    int pid;
    for (ProcessBase* child : this->childs_) 
    {
      pid = fork();
      if (pid == 0) 
      {
        child->Execute();
      }
      if (pid < 0)
      {
        child->PrintErrorMessage(this->name_);
      } 
    }
    sleep(TIME_SLEEP);
    for (ProcessBase* child : this->childs_) 
    {
      wait(NULL);
    }
    exit(EXIT_SUCCESS);
  }
};

int main() 
{
  ProcessBase* pid_g = new ProcessLead(PROCESS_G);
  ProcessBase* pid_f = new ProcessLead(PROCESS_F);
  ProcessBase* pid_e = new ProcessLead(PROCESS_E);
  ProcessBase* pid_c = new ProcessLead(PROCESS_C);

  std::list<ProcessBase*> childs_b = {pid_e, pid_f};
  ProcessBase* pid_b = new ProcessParent(PROCESS_B, childs_b);

  std::list<ProcessBase*> childs_d = {pid_g};
  ProcessBase* pid_d = new ProcessParent(PROCESS_D, childs_d);

  std::list<ProcessBase*> childs_a = {pid_b, pid_c, pid_d};
  ProcessBase* pid_a = new ProcessParent(PROCESS_A, childs_a);

  pid_a->Execute();

  return EXIT_SUCCESS;
}