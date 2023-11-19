<h2 style=color:purple>Automatización</h2>

El backend incluye módulos para automatizar dos tareas cruciales:

_Estos módulos son independientes del backend y no son necesarios para levantar el servidor_

1. Inyectar Batallas de Jugadores en la Base de Datos de MongoDB

    * En el directorio scripts, el archivo injection.sh ejecuta el módulo de Python llamado db_injection. No requiere nada para empezar, ya que obtiene automáticamente la ruta de la aplicación. Simplemente ejecútalo:

    ```console
    $ scripts/injection.sh
    ```


-**Detalles Técnicos**

El propio módulo de Python crea un bucle infinito asíncrono que ejecuta una función a intervalos regulares utilizando APScheduler.

Use los parámetros 'interval' y 'minutes' para definir cada cuánto tiempo debe ejecutarse la función:

```python
scheduler.add_job(repeater,'interval', minutes=1)
```

2. Eliminar Batallas Residuales

    * Cuando se elimina un track, todas las batallas registradas con ese track permanecen en la base de datos. Es recomendable eliminarlas. Para ello seguir estos pasos:

        * Establece la ruta de la aplicación y del entorno virtual en el script eliminator.sh.

        * Crea un cronjob para que se ejecute periódicamente; aquí tienes un ejemplo de ejecución diaria a las 12am:

    ```
    0 0 * * * ruta/al/script/eliminator.sh
    ```

-**Detalles Técnicos**

Para hacer que el eliminator.sh funcione debe tener configurada una base de datos de redis y que cada vez que se elimine un track esta este funcionando.

* En el módulo db_client puede configurar la localizacion de su base de datos de redis 

* Cuando se elimina un track el trackId se guarda en una lista en la db, cuando se ejecuta el eliminator.sh este lee la lista y elimina todas las batallas que contengan dichos trackIds