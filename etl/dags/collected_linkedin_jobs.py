import time

import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta


args = {
    'owner': 'danhphan',
    'email': ['dan.phan.mq@gmail.com'],
    'retries': 1,
    'start_date': days_ago(2),
}

dag = DAG('collected_linkedin_jobs', default_args=args, schedule_interval=timedelta(days=1))

# PATH_SCRIPT = "/usr/local/airflow/dags/tasks"
PATH_SCRIPT = "/home/airflow/gcs/dags/tasks"

task1 = BashOperator(
    task_id = "crawl_new_job_list",
    bash_command = f"python {PATH_SCRIPT}/lk_crawl_new_job_list.py",
    dag = dag,
)

task2 = BashOperator(
    task_id = "clean_new_job_list",
    bash_command = f"python {PATH_SCRIPT}/lk_clean_new_job_list.py",
    dag = dag,
)

task3 = BashOperator(
    task_id = "append_to_full_jobs",
    bash_command = f"python {PATH_SCRIPT}/lk_append_to_full_jobs.py",
    dag = dag,
)

task1 >> task2 >> task3