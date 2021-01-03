*************
Configuration
*************

CH Gallery provides some sane default configuration but you can override it's default values with your own config file.
Just place the file named ``config.py`` in application instance directory.

.. todo:: More about config file and different directories to fetch configuration from.

``SECRET_KEY`` - This is probably the first option you will want to change. Set your secret key and keep it **secret**!

``DATABASE`` - CH Gallery uses SQLAlchemy as a database backend so it's database independent. Value for this configuration
option must be a string valid for SQLALchemy config. Examples include
::

   # Sqlite
   DATABASE = 'sqlite:///path_to_db.sqlite'

   # PostgreSQL
   DATABASE = 'postgresql+psycopg2://dbuser:dbpass@localhost/dbname'

   # MySQL
   DATABASE = 'mysql+mysqlconnector://dbuser:dbpass@localhost/dbname'

In case you want to use engine other than *Sqlite* (which is provided by Python itself) you have to install appropriate
database driver. For *Posgresql*::

   $ pip install psycopg2

And for *MySQL*::

   $ pip install mysqlclient mysql-connector-python

The default engine as well as engine used for testing is *Sqlite*.

``REGISTRATION_DISABLED`` - Set it to ``True`` if you don't want to allow new users to use registration form and
authorize in the system. Defaults to ``False``.

``UPLOAD_PATH`` - The directory for uploaded images. Defaults to::

   UPLOAD_PATH = os.path.join(app.instance_path, 'uploads')
