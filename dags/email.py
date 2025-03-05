from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.email import EmailOperator

def print_hello():
    return "Hello World!"

default_args = {
    'owner':'ian',
    'start_date':datetime(2025,3,5),
}

with DAG(
    dag_id='email_alert_example',
    schedule=None,
    default_args=default_args,
) as dag:
    email = EmailOperator(
        task_id='email_alert',
        to='i.iyanmutuma@gmail.com',
        subject='Email Alert',
        html_content="""<h3>Email Test</h3>""",
    )

    dummy_operator = DummyOperator(
        task_id = 'dummy_task',
        retries = 3,
        dag = dag,
    )

    hello_operator = PythonOperator(
        task_id='hell_task',
        python_callable = print_hello,
        dag = dag
    )

    email >> dummy_operator >> hello_operator