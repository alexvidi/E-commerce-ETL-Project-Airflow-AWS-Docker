import sys
import os

# Ensure the project's root directory is in sys.path for proper module imports
sys.path.append("/mnt/c/Users/alexv/E-commerce ETL Project Airflow AWS Docker")

# Import required modules
from config.settings import S3_BUCKET, S3_KEY, TRANSFORMED_DATA_FILE
from airflow.providers.amazon.aws.hooks.s3 import S3Hook  

def load_data_to_s3():
    """
    Uploads the transformed data file to Amazon S3.

    Returns:
        dict: A dictionary containing the upload status, file name, and bucket.

    Raises:
        Exception: If there is an error during the file upload.
    """
    try:
        print(f"Starting upload to S3: {S3_BUCKET}/{S3_KEY}")
        s3_hook = S3Hook(aws_conn_id='aws_default')

        # Load the transformed data file to S3
        s3_hook.load_file(
            filename=TRANSFORMED_DATA_FILE,
            key=S3_KEY,
            bucket_name=S3_BUCKET,
            replace=True
        )

        print(f"File successfully uploaded to s3://{S3_BUCKET}/{S3_KEY}")
        return {
            'status': 'success',
            'file': S3_KEY,
            'bucket': S3_BUCKET
        }
    except Exception as e:
        print(f"Error uploading data to S3: {str(e)}")
        raise

# Entry point for the script
if __name__ == "__main__":
    load_data_to_s3()


