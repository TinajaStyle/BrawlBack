<h2 style=color:red>Testing</h2>

Lo único que hace falta para testear y ver que todo este yendo bien es:

* Crear un **usuario** en la base de datos y guardar el **JWT** recivido en el .env 

* Actualizar la **url** donde montaste el backend en el .env (probablemente _localhost:8000_)

* En el caso de **test_app** tendrás que actualizar los campos **name** y **password** con los creados anteriormente

* En el caso de **test_player** tendrás que actualizar los campos **player** y **tag** y tener un **track** al tag declarado (para saber como crear un track mirar la documentación de Swagger UI)

* En el caso de **test_track** lo único es actualizar el campo **tag**

* Finalmente para testear el **websocket** puedes actualizar la **url** (si es necesario) y el **tag** con uno que este siendo *trackeado*