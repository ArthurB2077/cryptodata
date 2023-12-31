from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('scrap_cryptopanic',
         default_args=default_args,
         schedule_interval=timedelta(minutes=5),
         start_date=datetime(2023, 10, 20),
         catchup=False) as dag:

    run_scraper_task = DockerOperator(
        task_id='run_scraper_task',
        image='v3-scraper:latest',
        api_version='auto',
        command="python main.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="v3_default",
        auto_remove="force",
        environment={
            'KAFKA_BROKER': 'kafka:9092'
        }
    )
