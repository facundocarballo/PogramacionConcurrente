# Java Style Guide

## Nombramientos
### Package
Los paquetes deben estar escritos solo en minúsculas.

**NO SE PUEDEN UTILIZAR:**
- Guiones bajos
- Camel Case
- Guiones medios

*Ejemplo*

    com.example.mipaquetejava

Solo hay que escribir el paquete en minúsculas.
### Archivos
Los nombres de archivos deben coincidir exactamente con el nombre de la clase que se esta escribiendo.
*Ejemplo*

    MiClase.java

### Clases

    class MiClase
    {
    }
 
### Variables

    diasDeLaSemana = 7

#### Constantes

    static final int ES_CONSTANTE = 7;

### Funciones

    void estaEsMiFuncion()
    {
    }

### Comentarios
#### Clases
Las clases que consideremos que son medias raras, que no se describen con su simple nombre; deberán incluir un breve comentario que indique porque se creo esta clase y como debe ser usada.

***Los comentarios de las clases deberán concentrarse en poder responder estas dos preguntas.***
 - Porque es necesaria esta clase?
 - Como puedo usar esta clase? 

#### Funciones
**La gran mayoría de** las funciones deberán tener comentarios que describan que hace la funcion y como utilizarla.
Omitir los comentarios en funciones si son funciones muy simples y obvias de entender. 

***Preferentemente que todas estén comentadas y que busquen responder estas dos preguntas.***
 - Porque es necesaria esta clase?
 - Como puedo usar esta clase? 

#### Variables
Preferentemente las variables no deben llevar comentarios, su propio nombre debe ser lo suficiente descriptivo para entender que almacena.

De todas formas, si vemos que una variable necesita un comentario; este debe ir arriba de la declaración de la variable.

*Ejemplo*

    // Esta variable almacenara la edad del usuario
    int ageOfUser;

### Formatos
- Máximo de 100 caracteres por linea de codigo
- 2 Espacios para identar