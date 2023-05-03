import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.util.Scanner;

public class Cliente 
{
    private static final String DIRECCION_SERVIDOR = "localhost";
    private static final int PUERTO_SERVIDOR = 5000;

    public static void main(String[] args) 
    {
        String mensaje = null;
        try 
        {
            // Inicializar el socket cliente y enviar el mensaje
            Socket socketCliente = new Socket(DIRECCION_SERVIDOR, PUERTO_SERVIDOR);
            //socketCliente.getOutputStream().write(mensaje.getBytes());

            // Leer la respuesta del servidor y procesar el mensaje
            Scanner entrada = new Scanner(socketCliente.getInputStream());
            boolean endCom = false;
            while(!endCom) 
            {
            	
            	String respuesta = entrada.nextLine();
                if(respuesta.equals("endCom")) 
                {
                	endCom = true;
                	continue;
                }
                	
            	System.out.println("Respuesta recibida del servidor: " + respuesta);
                	
                int caracteresTotales = respuesta.length();
                int cantidadLetras = 0;
                int cantidadDigitos = 0;
                int cantidadOtros = 0;
                for (char c : respuesta.toCharArray()) 
                {
                    if (Character.isLetter(c)) 
                    {
                        cantidadLetras++;
                    } else if (Character.isDigit(c)) 
                    {
                        cantidadDigitos++;
                    } else 
                    {
                        cantidadOtros++;
                    }
                }

                // Mostrar los resultados por pantalla
                System.out.println("Cantidad de caracteres totales: " + caracteresTotales);
                System.out.println("Cantidad de letras: " + cantidadLetras);
                System.out.println("Cantidad de dígitos: " + cantidadDigitos);
                System.out.println("Cantidad de caracteres que no son letra ni dígito: " + cantidadOtros);
                System.out.println("--------------------------------------------------------------------------");
            }
            
            

            // Cerrar los recursos
            entrada.close();
            socketCliente.close();
        } 
        catch (IOException e) 
        {
            e.printStackTrace();
        }
    }
}