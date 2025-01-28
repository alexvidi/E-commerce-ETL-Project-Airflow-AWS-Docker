# Imports required modules for DAG and operators
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import json
import pandas as pd
import boto3

# Function that fetches data from an API and saves it as a JSON file
def extract_data():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Saves the fetched data to a JSON file
        with open('/tmp/products.json', 'w') as f:
            json.dump(data, f)
    else:
        raise ValueError(f"Error connecting to the API: {response.status_code}")

# Function that transforms the fetched data
def transform_data():
    # Reads data from the JSON file
    data = pd.read_json('/tmp/products.json')

    # Adds a simulated sales field to the data (e.g., multiplying price by a factor)
    data['sales'] = data['price'] * 10  # Example: assume selling 10 units of each product

    # Calculates total sales by category
    total_sales_by_category = data.groupby('category')['sales'].sum()

    # Saves the transformed metrics to a CSV file
    total_sales_by_category.to_csv('/tmp/total_sales_by_category.csv')    

# Function that uploads the transformed data to Amazon S3
def load_data():
    # Specifies the name of the transformed file
    transformed_file = '/tmp/total_sales_by_category.csv'
    # Specifies the S3 bucket name and the file key
    bucket_name = 'bucket-project-etl'  # Replace with your real bucket name
    s3_key = 'data/total_sales_by_category.csv'

    # Creates the S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id='AKIAZQ3DULIUK7A4DZOX',
        aws_secret_access_key='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'
    )

    # Uploads the file to S3
    s3.upload_file(transformed_file, bucket_name, s3_key)
    print(f"File successfully uploaded to s3://{bucket_name}/{s3_key}")

# Defines the DAG (Directed Acyclic Graph) structure
with DAG(
    dag_id="ecommerce_pipeline",
    default_args={
        # Specifies the DAG's start date
        'start_date': datetime(2025, 1, 28),
        # Number of retries in case of failure
        'retries': 1,
    },
    # Specifies that the DAG will not run on a schedule
    schedule_interval=None,
    # Indicates that previous runs should not catch up
    catchup=False,
) as dag:

    # Defines a dummy start task
    start_task = DummyOperator(task_id='start')
    # Defines a dummy end task
    end_task = DummyOperator(task_id='end')

    # Sets the dependency between start and end tasks
    start_task >> end_task

# Adds the actual tasks to the DAG
# Task that extracts data
extract_task = PythonOperator(task_id='extract_data', python_callable=extract_data)
# Task that transforms the data
transform_task = PythonOperator(task_id='transform_data', python_callable=transform_data)
# Task that loads the data to S3
load_task = PythonOperator(task_id='load_data', python_callable=load_data)

# Sets the sequence of tasks in the DAG
start_task >> extract_task >> transform_task >> load_task >> end_task

