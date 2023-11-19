<h2 style=color:red>Testing</h2>

The only thing needed to test and ensure that everything is working correctly is:

* Create a **user** in the database and save the received **JWT** in the .env file.

* Update the **URL** where you hosted the backend in the .env file (probably *localhost:8000*).

* In the case of **test_app**, you will need to update the **name** and **password** fields with the ones created earlier.

* In the case of **test_player**, update the **player** and **tag** fields and have a **track** associated with the declared tag (to learn how to create a track, refer to the Swagger UI documentation).

* For **test_track**, the only thing is to update the **tag** field.

* Finally, to test the **WebSocket**, you can update the **URL** (if necessary) and the **tag** with one that is being **tracked**.