<h2 style=color:purple>Automation</h2>

The backend includes modules for automating two crucial tasks:

_These modules are independent of the backend and are not necessary to start the server._

1. Injecting Player Battles into the MongoDB Database:

    * In the scripts directory, the injection.sh file launches the Python module named db_injection. It requires nothing to start as it automatically obtains the app's path. Simply execute it:

    ```console
    $ scripts/injection.sh
    ```


-**Technical Details**

The Python module itself creates an asynchronous infinite loop that executes a function at regular intervals using APScheduler.

Use the 'interval' and 'minutes' parameters to define how often the function should run:

```python
scheduler.add_job(repeater,'interval', minutes=1)
```

2. Eliminating Residual Battles:

    * When a track is deleted, all battles recorded with that track remain in the database. It's advisable to remove them. Follow these steps:

        * Set the app and virtual environment path in the eliminator.sh script.

        * Create a cronjob to run periodically; here's an example for daily execution at 12 am:

    ```
    0 0 * * * ruta/al/script/eliminator.sh
    ```

-**Technical Details**

To make eliminator.sh work, you must have a configured Redis database, and it should be operational each time a track is deleted.

* In the db_client module, you can configure the location of your Redis database.

* When a track is deleted, the trackId is saved in a list in the database. When eliminator.sh is executed, it reads the list and deletes all battles containing those trackIds.