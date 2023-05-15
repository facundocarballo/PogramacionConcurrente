import java.io.Serializable;

public class Respuesta implements Serializable 
{
  private String caractTotales;
  private String cantLetras;
  private String cantDigitos;
  private String cantidadOtros;

  public Respuesta(String caractTotales, String cantLetras, String cantDigitos, String cantidadOtros)
  {
    this.caractTotales = caractTotales;
    this.cantLetras = cantLetras;
    this.cantDigitos = cantDigitos;
    this.cantidadOtros = cantidadOtros;
  }

  @Override
  public String toString()
  {
    return caractTotales + cantLetras + cantDigitos + cantidadOtros;
  }
  
  // Getter methods for private fields
  public String getCaractTotales()
  {
    return caractTotales;
  }

  public String getCantLetras()
  {
    return cantLetras;
  }

  public String getCantDigitos()
  {
    return cantDigitos;
  }

  public String getCantidadOtros()
  {
    return cantidadOtros;
  }
}
