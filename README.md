# ETL E-commerce Pipeline

## Project Description

This project implements an ETL (Extract, Transform, Load) pipeline using Apache Airflow, designed to process simulated e-commerce data. 
The pipeline automates data extraction from an API, transforms it into meaningful metrics, and stores it in Amazon S3 for further analysis.

---

## Technologies and Tools Used

- **Apache Airflow**: Orchestrates the pipeline and manages ETL tasks.
- **Python**: The primary programming language for pipeline logic.
- **Pandas**: A library used for data manipulation and analysis during the transformation step.
- **Boto3**: AWS SDK for Python, used to integrate with Amazon S3.
- **Amazon S3**: Cloud storage service for storing processed data.
- **requests**: A Python library for making HTTP requests and fetching data from the API.
- **Docker**: Runs Airflow and its components in a containerized environment.
- **GitHub**: Version control and source code repository.

---

## ETL Pipeline Workflow

1. **Extraction (Extract)**:  
   Product data is fetched from the [Fake Store API](https://fakestoreapi.com) and saved as a JSON file.
   
2. **Transformation (Transform)**:  
   - The extracted data is loaded using Pandas.  
   - A simulated sales field is generated.  
   - Total sales by category are calculated and saved as a CSV file.

3. **Loading (Load)**:  
   The processed data is uploaded to an Amazon S3 bucket using the Boto3 client.

---

## Project Structure

```plaintext
etl_ecommerce/
├── dags/
│   ├── ecommerce_pipeline.py  # Airflow pipeline code
├── requirements.txt           # Required dependencies
├── README.md                  # This file
