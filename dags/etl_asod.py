import os
import pathlib

import requests

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from bs4 import BeautifulSoup

from datetime import date, timedelta

dag_owner = "ian"

   
default_args = {
    'owner':dag_owner,
    'depends_on_past':False,
    'retries':2,
    'retry_delay':timedelta(minutes=5)
}

@dag(
    dag_id='download_apod_image',
    default_args=default_args,
    description='download and notify',
    start_date=days_ago(0),
    schedule_interval="@daily",
    catchup=True,
    tags=['None']
)
def apod_dag():
    @task()
    def get_picture():
        current_dir = os.getcwd()
        image_dir = os.path.join(current_dir,"images")
        pathlib.Path(image_dir).mkdir(parents=True,exist_ok=True)

        #api_key = "DEMO_KEY"
        api_key = "SNR99N7MPOjyWYUw0SKZzzLueb5LLVmFl8ZBwAzu"

        url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
        response = requests.get(url).json()

        today_image_url = response['url']
        today_image_page = requests.get(today_image_url)

        soup = BeautifulSoup(today_image_page.content,"html.parser")

        image_tag = soup.find('img')
        if image_tag:
            image_url = image_tag['src']
            image_response = requests.get("https://apod.nasa.gov/apod/image/1803/AstroSoM/" + image_url)

            if image_response.status_code == 200:
                with open(f'{image_dir}/todays_image_{date.today()}.png',"wb") as f:
                    f.write(image_response.content)
    

    notify_task = BashOperator(
        task_id='notify',
        bash_command='echo "Images for $today_date have been added!"'
    )
    
    get_picture() >> notify_task

apod_dag()
