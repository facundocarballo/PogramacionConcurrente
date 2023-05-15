# Python Style Guide

## Nombramientos

### Archivos
Los nombres de archivos deben estar escritos todos en letras minúsculas. Las palabras separadas por guiones bajo
*Ejemplo*

    my_class.py

### Clases
    public class ClasePublic
    {
    }
    
    private class _ClasePrivada
    {
    }
    
### Variables
    dias_de_la_semana = 7

#### Atributos
##### Proteced

    _dias_de_la_semana = 7

##### Private

     __dias_de_la_semana = 7
##### Public
    dias_de_la_semana = 7

#### Constantes
    ES_CONSTANTE= 7;

### Funciones
##### public
    def esta_es_mi_funcion():
##### protected
    def _esta_es_mi_funcion():

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

    #Esta variable almacenara la edad del usuario
    age_of_user

### Formatos
- Máximo de 40 caracteres por linea de codigo
- 2 Espacios para identar