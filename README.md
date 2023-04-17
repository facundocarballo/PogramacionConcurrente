
# Grupo M5 - Programación Concurrente
### Integrantes:
| Nombre | DNI |
|--|--|
| Facundo Nicolas Carballo | 42.774.931 |
| Federico Pucci | 41.106.855 |
| Alejo Lencinas | 41.427.410 |
| Ignacio Romero | 44.209.416 |
| Gian Luca Simonetti | 41.716.091 |
----
# Coding Style

 - [C++](#c)
 - [Java](#java)
 - [Python](#python)

<a name="c" />

# C++
## Nombramientos

  

### Archivos

Los nombres de archivos deben estar escritos todos en letras minúsculas. Las palabras separadas por guiones bajo

*Ejemplo*

  

    my_class.c

  

### Clases, Tipos, Estructuras y Enums

Deben empezar con letras mayúsculas por cada nueva palabra.

NO UTILIZAR GUIONES BAJO.

  

### Variables

Las variables deben estar todas en minúscula y separadas por guiones bajo entre cada palabra

*Ejemplo*

  

    std::string table_name;

  

#### Atributos

Los atributos de una clase deben nombrarse igual que las variables, pero terminando con un guion bajo al final.

*Ejemplo*

  

    std:string table_name_;

  

#### Constantes

Las constantes deben comenzar con la letra **k** y luego continuar con una letra mayuscula por cada nueva palabra.

*Ejemplo*

  

    const int kDiasDeLaSemana = 7;

  

### Funciones

Las funciones deben empezar siempre con letra mayúscula y volver a utilizar una mayúscula cada vez que se cambia de palabra.

*Ejemplo*

  

    void EstaEsMiFuncion();

#### Getters y Setters

Estas son las únicas funciones que hay se escriben como las variables

*Ejemplo*

  

    void set_count(int count);
    
    int get_count();

  

### Macros

Las macros van todas escritas con mayusculas y las palabras separadas por guiones bajos.

*Ejemplo*

  

    #define FACU_MACRO 3

  

### Comentarios

Siempre utilizar el mismo tipo de comentario.

O usamos **//** o usamos **/* */**, pero siempre tiene que usarse el mismo.

  

***GOOGLE RECOMIENDA USAR //***

  

#### Archivos

Siempre comentar la primera linea de cada archivo con la licencia que estamos utilizando.

*Ejemplo*

  

    // (c) 2023 M5 - Progamacion Concurrente
    
    //This code is licensed under MIT license (see LICENSE.txt for details)

  

Luego es recomendable hacer un breve comentario sobre lo que contiene el archivo en cuestión.

  

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

Preferentemente las variables no deben llevar comentarios, su propio nombre debe ser lo suficiente descriptivo para enteder que almacena.

  

De todas formas, si vemos que una variable necesita un comentario; este debe ir arriba de la declaracion de la variable.

  

*Ejemplo*

  

// Esta variable almacenara la edad del usuario

    int age_of_user;

  

### Formatos

- Máximo de 80 caracteres por linea de codigo

- 2 Espacios para identar

- Corchetes debajo **SIEMPRE**

  

## Recomendaciones

### Clases

#### Orden de Declaración

    class Base
    
    {
    
    // 1- Typedefs
    
    typedef int SOCKET;
    
    // 2- Estructuras
    
    struct myStruct
    
    {
    
    int id;
    
    int value;
    
    }
    
    // 3- Constantes Estaticas
    
    static const int value_ = 1;
    
    // 4- Funciones Factory
    
    // 5- Constructores
    
    // 6- Destructor
    
    // 7- Funciones
    
    // 8- Atributos
    
    }

Seguir esta secuencia tanto para los **public, private** y **protected.**

  

    class Base
    
    {
    
    public:
    
    // 1- Typedefs
    
    typedef int SOCKET;
    
    ...
    
    protected:
    
    // 1- Typedefs
    
    typedef int SOCKET;
    
    ...
    
    private :
    
    // 1- Typedefs
    
    typedef int SOCKET;
    
    ...
    
    }

  
  

#### Constructores

- No llamar a métodos virtuales dentro del constructor.

- No inicializar nada que pueda fallar, ya que no podremos manejar ese error de forma correcta.

- Si necesitamos llamar a métodos virtuales para instanciar nuestra clase, es preferible tener una funcion **Init()** que llame a esos métodos virtuales.

  

En conclusión, hay que evitar a todo costa llamar a métodos virtuales dentro de los constructores de una clase.

  

#### Herencia

- Las herencias deben ser preferentemente publicas. Si tenemos herencias privadas, hay que asegurarnos de crear una instancia de la Clase Base como un atributo de nuestra Clase.

- No abusar de las herencias, a veces crear una composición es mas apropiado.

- Limitar el uso de ***protected*** a solo aquellas funciones que puedan ser accedidas por sub clases.

  

### Estructuras

Utilizar **Structs** solo para objetos pasivos que contengan datos. Para todo lo demás, es recomendable utilizar Clases.

  

### Tuplas y Pares

Evitar el uso de Tuplas y Pares, es mejor usar una Estructura.

<a name="Java" />

# Java

  

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

<a name="python" />

# Python

  

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
