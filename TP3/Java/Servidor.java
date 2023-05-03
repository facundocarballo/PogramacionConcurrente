import java.io.IOException;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;

public class Servidor 
{
    private static final int PUERTO = 5000;

    public static void main(String[] args) 
    {
        try 
        {
            
            ServerSocket socketServidor = new ServerSocket(PUERTO);
            System.out.println("Servidor iniciado en el puerto " + PUERTO);

            
            System.out.println("Esperando conexión de un cliente...");
            Socket socketCliente = socketServidor.accept();
            System.out.println("Cliente conectado desde la dirección " + socketCliente.getInetAddress());
            boolean endCom = false;
            Scanner entrada = new Scanner(System.in);
            
            OutputStream salida = socketCliente.getOutputStream();
            
            while(!endCom) 
            {
            	System.out.println("Ingrese el mensaje para el usuario:");
            	System.out.print(">");
            	String mensaje = entrada.nextLine();
                mensaje = mensaje+"\n";
            	if(mensaje.equals("endCom\n")) 
            	{
            		salida.write(mensaje.getBytes());
                	endCom = true;
                	continue;
                }
                salida.write(mensaje.getBytes());
                System.out.println("Mensaje enviado al cliente: " + mensaje);
            }
            

            
            entrada.close();
            salida.close();
            socketCliente.close();
            socketServidor.close();
        } 
        catch (IOException e) 
        {
            e.printStackTrace();
        }
    }
}