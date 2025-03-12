import sys
import os
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta

# Ensure the root directory is included in sys.path for module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import ETL functions and configurations
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.load_s3 import load_data_to_s3  
from config.settings import S3_BUCKET, S3_KEY, FAKE_STORE_API, RAW_DATA_FILE

# Default configuration settings for the DAG
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 28),
}

# Define the ETL pipeline DAG
with DAG(
    dag_id='ecommerce_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for processing e-commerce data',
    schedule='0 6 * * *',  # Runs daily at 6:00 AM
    catchup=False,
    tags=['ecommerce', 'etl', 'data-engineering']
) as dag:
    
    # Start task - Marks the beginning of the pipeline
    start = EmptyOperator(task_id='start_pipeline')
    
    # Task to check if the API is available before extracting data
    check_api = HttpSensor(
        task_id='check_api_availability',
        http_conn_id='fake_store_api',
        endpoint='products',
        response_check=lambda response: response.status_code == 200,
        poke_interval=30,
        timeout=300
    )

    # Task to extract data from the API
    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data
    )
    
    # Task to transform the extracted data
    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data
    )
    
    # Task to load the transformed data to S3
    load = PythonOperator(
        task_id='load_data_to_s3',
        python_callable=load_data_to_s3
    )
    
    # Task to verify the S3 file exists
    verify_s3_load = S3KeySensor(
        task_id='verify_s3_file_exists',
        bucket_key=S3_KEY,
        bucket_name=S3_BUCKET,
        aws_conn_id='aws_default',
        timeout=300,
        poke_interval=60
    )
    
    # End task - Marks the end of the pipeline
    end = EmptyOperator(task_id='end_pipeline')
    
    # Define the execution order of tasks in the DAG
    start >> check_api >> extract >> transform >> load >> verify_s3_load >> end

