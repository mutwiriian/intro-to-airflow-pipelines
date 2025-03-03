This project demonstrates a basic Airflow pipeline that extracts the Astronomer Picture of the Day from the James Webb Telescope, loads into
local storage and sends an email notification on success

The image is extracted by parsing the page using BeautifulSoup to extract
the image.

The TaskFlow and traditional APIs are combined to define the structure of the DAG.
To ensure the projects runs successfully, follow the installation instructions on the official Airflow[] documentation and then install the `airflowctl` library in the `uv` environment.

By default, Airflow uses SQLite as the Metadata Database which does not allow concurrent writes. Install and run the PostgreSQL server locally as a superuser. Install the `apache-airflow-providers-postgres` and `psycopg2` libraries to enable Airflow connections. 

Run the following setup queries to create the database and user permissions:

1. create database airflow_db;
2. \c airflow_db; #change to airflow_db
2. create role <user> with password 'password';
3. alter role <user> set client_encoding to 'utf8';
4. alter role <user> set default_transaction_isolation to "read commited";
5. alter role <user> set timezone to 'UTC';
6. grant all privileges on schema public to <user>;

To ensure Airflow connects to our database and executes the tasks update the `airflow.cfg` file by setting `executor = LocalExecutor` and `sql_alchemy_conn = postgresql+psycopg2:/user:password@localhost:5432/airflow_db`

To run the database migration execute `airflow migrate`

Run `airflowctl start` and access the webserver UI to trigger the pipeline
