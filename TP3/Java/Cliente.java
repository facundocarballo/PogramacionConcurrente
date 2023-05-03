import java.io.IOException;
import java.io.ObjectInputStream;
import java.net.Socket;

public class Cliente 
{
    private static final String DIRECCION_SERVIDOR = "localhost";
    private static final int PUERTO_SERVIDOR = 5000;

    public static void main(String[] args) throws ClassNotFoundException 
    {
        String mensaje = args[0] + "\n";

        try 
        {
            Socket socketCliente = new Socket(DIRECCION_SERVIDOR, PUERTO_SERVIDOR);
            socketCliente.getOutputStream().write(mensaje.getBytes());

            ObjectInputStream entrada = new ObjectInputStream(socketCliente.getInputStream());
            Respuesta respuesta = (Respuesta) entrada.readObject();
            System.out.println(respuesta);

            entrada.close();
            socketCliente.close();
        } catch (IOException e) 
        {
            e.printStackTrace();
        }
    }
}
