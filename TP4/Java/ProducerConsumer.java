package TP4.Java;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ProducerConsumer {
    final static Integer MODULE = 100;
    final static Integer TIME_SLEEP = 500;
    final static Integer INIT_VALUE = 1;

    private static Integer valorCompartido = null;

  public static void main(String[] args) 
  {
    Lock lock = new ReentrantLock();
    Condition condition = lock.newCondition();
    int limit = Integer.parseInt(args[0]);

    Thread producer = new Thread(() -> 
    {
      for (int i = INIT_VALUE; i <= limit; i++) 
      {
        int valor = i % MODULE;

        lock.lock();
        try 
        {
          valorCompartido = valor;
          System.out.println("Productor produjo el valor " + valor);
          condition.signal();
        } 
        finally 
        {
          lock.unlock();
        }

        try 
        {
          TimeUnit.MILLISECONDS.sleep(TIME_SLEEP);
        } 
        catch (InterruptedException e) 
        {
          e.printStackTrace();
        }
      }
    });

    Thread consumer = new Thread(() -> 
    {
      for (int i = INIT_VALUE; i <= limit; i++) 
      {
        lock.lock();
        try 
        {
          while (valorCompartido == null) 
          {
            condition.await();
          }

          int valor = valorCompartido;
          valorCompartido = null;
          System.out.println("Consumidor consumió el valor " + valor);
        } 
        catch (InterruptedException e) 
        {
          e.printStackTrace();
        } 
        finally 
        {
          lock.unlock();
        }
      }
    });

    // Iniciamos ambos hilos
    producer.start();
    consumer.start();
  }
}
