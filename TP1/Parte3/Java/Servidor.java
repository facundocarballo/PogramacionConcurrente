import java.io.IOException;
import java.io.ObjectOutputStream;
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

            Scanner entrada = new Scanner(socketCliente.getInputStream());
            ObjectOutputStream salida = new ObjectOutputStream(socketCliente.getOutputStream());

            String mensajeCliente = entrada.nextLine();
            System.out.println(mensajeCliente);

            int caracteresTotales = mensajeCliente.length();
            int cantidadLetras = 0;
            int cantidadDigitos = 0;
            int cantidadOtros = 0;

            for (char c : mensajeCliente.toCharArray()) 
            {
                if (Character.isLetter(c)) 
                {
                    cantidadLetras++;
                } 
                else if (Character.isDigit(c)) 
                {
                    cantidadDigitos++;
                } 
                else 
                {
                    cantidadOtros++;
                }
            }

            String s1 = "Cantidad de caracteres totales: " + caracteresTotales + "\n";
            String s2 = "Cantidad de letras: " + cantidadLetras + "\n";
            String s3 = "Cantidad de dígitos: " + cantidadDigitos + "\n";
            String s4 = "Cantidad de caracteres que no son letra ni dígito: " + cantidadOtros + "\n";
            Respuesta respuesta = new Respuesta(s1, s2, s3, s4);
            salida.writeObject(respuesta);

            entrada.close();
            salida.close();
            socketCliente.close();
            socketServidor.close();
        } catch (IOException e) 
        {
            e.printStackTrace();
        }
    }
}