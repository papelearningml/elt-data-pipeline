from datetime import datetime
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess
import os

# Récupération des chemins depuis les variables d'environnement
AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')
PROJECT_DIR = os.environ.get('PROJECT_DIR', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DBT_PROFILES_DIR = os.environ.get('DBT_PROFILES_DIR', os.path.expanduser('~/.dbt'))

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

def run_elt_script():
    script_path = os.path.join(AIRFLOW_HOME, "elt_script", "elt_script.py")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)

dag = DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2023, 8, 3),
    catchup=False,
)

t1 = PythonOperator(
    task_id='run_elt_script',
    python_callable=run_elt_script,
    dag=dag,
)

network_test = BashOperator(
    task_id='network_test',
    bash_command='nc -zv destination_postgres 5432',
    dag=dag
)

t2 = DockerOperator(
    task_id='dbt_run',
    image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
    command=[
        "run",
        "--profiles-dir", "/home/airflow/.dbt",
        "--project-dir", "/opt/airflow/custom_postgres",
    ],
    docker_url="unix://var/run/docker.sock",
    network_mode="elt_network",
    api_version='auto',
    auto_remove=True,
    mounts=[
        Mount(
            source=f"{PROJECT_DIR}/custom_postgres",
            target="/opt/airflow/custom_postgres",
            type='bind',
        ),
        Mount(
            source=DBT_PROFILES_DIR,
            target="/home/airflow/.dbt",
            type='bind',
        ),
    ],
    mount_tmp_dir=False,
    tty=True,
    environment={
        'DBT_PROFILES_DIR': '/home/airflow/.dbt',
    },
    dag=dag,
)

t1 >> network_test >> t2