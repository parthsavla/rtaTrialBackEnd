### MODELS

## DB INSTANCE
- We will be using <db> instance of sqlalchemy  to create the models
- db instance contains all the functions and helpers from both <sqlalchemy> and <sqlalchemy.orm>
- It provides <Model> class that is used to declare models.

## DB MIGRATIONS
- With Flask-Migrate installed, we use flask cli as follows
- To create a migrations repo we use the following command (must be added to version control).
- 
* `$ flask db init` *

- To generate initial migration
* `$ flask db migrate -m "Initial migration."` *

- Apply the migrations to the db
* `$ flask db upgrade` * 

- NOTE: Each time the db changes, repeat the `migrate` & `upgrade` commands. To see all the commands that are available `$ flask db --help`