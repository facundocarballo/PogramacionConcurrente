package processtree;

import java.io.IOException;

public class ProcessTree 
{
  public static void main(String[] args) throws IOException, InterruptedException 
  {
    ProcessHandle process = ProcessHandle.current();
    long pid = process.pid();
    long ppid = process.parent().get().pid();
    System.out.println("Soy el proceso: " + pid + ", Mi papa es: " + ppid);

    int level = Integer.parseInt(args[1]);
    if (level == 2) 
    {
      Thread.sleep(10000);
      return;
    }

    int childrenNum = Integer.parseInt(args[0]);

    Process childs[] = new Process[childrenNum];

    for (int i = 1; i <= childrenNum; i++) 
    {
      ProcessBuilder pb =
          new ProcessBuilder(
              "java", "ProcessTree.java", String.valueOf(childrenNum - i), String.valueOf(level + 1));
      pb.inheritIO();
      childs[i - 1] = pb.start();
    }
    Thread.sleep(10000);
    for (int i = 0; i < childs.length; i++) 
    {
      childs[i].waitFor();
    }
  }
}
