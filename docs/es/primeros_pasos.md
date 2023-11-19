### Instalar los requerimientos

Primero es necesario instalar las dependencias, estas las puede encontrar en el archivo requirements.txt (las versiones son las que usé, pero se pueden usar algunas anteriores).

_recomendacion: usar un entorno virtual para instalar las dependencias_

```console
$ pip install requirements.txt

--->100%
```

### Creacion del .env

La información sensible debe ir en un archivo .env pero no se preocupe la conexion con el código ya esta hecha :) solo tienes que declarar dichas variables de entorno. Hay un ejemplo de cómo debe ser el .env en esté directorio

* **DB_URL**: es la variable encargada de almacenar la url de la base de datos de mongodb (más adelante se aborda este tema)

* **BRAWL_API_TOKEN**: aquí se almacena el token que se genera en la web de desarrollo de Brawl Stars [1](developer.brawlstars.com)

* **BRAWL_API_URL**: contiene la url de la api de Brawl Stars [1](developer.brawlstars.com")

* **ALGORITHM**: es el tipo de algoritmo para encriptar los JWT

* **UNLOCK**: es la clave para encriptar los JWT (más adelante se aborda este tema)

* **TEST_TOKEN**: contiene el token que se usa para los test, este token es generado por el propio backend cuando te logeas

* **API_URL**: es la url al propio backend (probablemente sea *localhost*)

### Conexión con Mongodb 

Para este backend he decidido usar mongodb ya que es una base de datos NOSQL más importantes actualmente, tiene compatibilidad con la programación asíncrona con su libreria **motor** y además tiene un plan gratuito para que puedas testear sin tener que configurar tú totalmente la base de datos. Más informacion en su [documentacion](https://www.mongodb.com/docs/)

### Generar Clave para JWT

Puedes generar una clave totalmente a tu gusto, desde ir a un sitio web hasta crearlo por consola como te presentare a continuación pero simpre lo más importante es que se trabaje con cuidado con este tipo de información

```console
$ openssl rand -hex 32
```

### Poner en marcha el servidor

Una vez este todo listo lo único que queda es ejecutar el **main.py** así de sencillo

```console
$ python3.11 main.py
```

### Mira la documentacion de Swagger UI

Puedes ir a localhost(si asi lo definiste) /documentation y allí encontraras toda la información de los router, cómo debes hacer las requests y que es lo que va a responder