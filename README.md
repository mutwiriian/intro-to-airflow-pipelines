# 
This project demonstrates a basic Airflow pipeline that extracts the Astronomer Picture of the Day from the James Webb Telescope,
loads into local storage and simulates sending an email notification on success

The image is extracted by parsing the page using **BeautifulSoup** to extract the image.

The TaskFlow and the traditional APIs are combined to define the structure of the DAG.
To ensure the projects runs successfully, create a **uv** environment, follow the [**Airflow**](https://airflow.apache.org/docs/apache-airflow/stable/index.html)  installation instructions and then install the [**airflowctl**](https://github.com/kaxil/airflowctl) .

By default, Airflow uses SQLite as the Metadata Database which does not allow concurrent writes. To get around this install and
run a PostgreSQL server locally as a superuser. 
Install the **apache-airflow-providers-postgres** and **psycopg2** libraries to enable Airflow connections. 
```
uv pip install apache-airflow-providers-postgres psycopg2
```

Run the following SQL setup queries to create the database and user permissions:

```
 create database airflow_db;
 \c airflow_db; #change to airflow_db
 create role <user> with password 'password';
 alter role <user> set client_encoding to 'utf8';
 alter role <user> set default_transaction_isolation to "read commited";
 alter role <user> set timezone to 'UTC';
 grant all privileges on schema public to <user>;
 ```

To ensure Airflow connects to our database and runs the tasks update the *airflow.cfg* file by setting 
`executor = LocalExecutor` and `sql_alchemy_conn = postgresql+psycopg2:/user:password@localhost:5432/airflow_db`

To run the database migration execute `airflow migrate`

Run `airflowctl start` and access the webserver UI to trigger the pipeline
