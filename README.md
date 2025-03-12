# E-commerce ETL Project with Airflow, AWS & Docker

##  Project Overview
This project implements a **fully automated ETL pipeline** using **Apache Airflow, AWS S3, and Docker**. The pipeline extracts product data from the Fake Store API, processes sales metrics, and uploads the transformed data to **Amazon S3** for further analysis.

The main objective is to **demonstrate a scalable and containerized ETL workflow** that can be deployed in real-world data engineering environments.

##  Architecture
```
 ┌───────────────────┐     ┌──────────────────┐     ┌───────────────┐     ┌──────────────┐
 │ Fake Store API   │ --> │ Extract Data    │ --> │ Transform Data │ --> │ Load to S3   │
 └───────────────────┘     └──────────────────┘     └───────────────┘     └──────────────┘
```
## Pipeline Stages:

**Extract** → Retrieves product data from the Fake Store API.

**Transform** → Processes sales metrics and categorizes data.

**Load** → Uploads transformed data to an **Amazon S3** bucket.

##  Technologies Used
- **Apache Airflow** Orchestrates the ETL workflow.
- **Docker** Manages Airflow services in containers.
- **AWS S3** Stores the processed data
- **Python (Pandas, Requests, Boto3)** Extracts, transforms, and loads the data.

##  Project Structure

```
E-COMMERCE ETL PROJECT AIRFLOW AWS DOCKER/
│── config/                    # Configuration files
│   ├── settings.py            # ETL settings (API URLs, S3 paths, etc.)
│
│── dags/                       # Airflow DAG definitions
│   ├── ecommerce_dag.py       # ETL DAG definition
│   ├── _pycache_/           # Python cache (ignored in Git)
│
│── data/                       # Data storage
│   ├── raw/                    # Raw extracted data
│   │   ├── products.json       # Extracted JSON data
│   ├── transformed/            # Transformed data
│   │   ├── total_sales_by_category.csv  # Processed sales metrics
│
│── docs/                       # Documentation and screenshots
│   ├── airflow_aws_api_connection.png
│   ├── amazon_s3_load_file_success.png
│   ├── dag_graph_success.png
│   ├── dag_list.png
│   ├── dag_tasks_success.png
│   ├── docker_desktop_containers.png
│
│── scripts/                    # ETL Python scripts
│   ├── extract.py              # Extracts data from API
│   ├── transform.py            # Transforms and processes data
│   ├── load_s3.py              # Loads processed data into S3
│   ├── _init_.py             # Marks directory as a package
│   ├── _pycache_/            # Python cache (ignored in Git)
│
│── venv/                       # Virtual environment (ignored in Git)
│
│── .gitignore                  # Files to exclude from Git
│── .env                        # Environment variables (not committed)
│── docker-compose.yaml         # Airflow and service configuration
│── Dockerfile                  # Custom Airflow image setup
│── README.md                   # Project documentation
│── requirements.txt            # Python dependencies
```

##  Setup & Installation
### Clone the Repository
```bash
git clone https://github.com/alexvidi/E-commerce-ETL-Project-Airflow-AWS-Docker.git
cd E-commerce-ETL-Project-Airflow-AWS-Docker
```
## Future Enhancements
 Connect to a database instead of storing files in S3.
 Implement real-time streaming with Kafka.
 Use dbt for transformations.