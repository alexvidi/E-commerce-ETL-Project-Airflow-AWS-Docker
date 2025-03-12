# Use the official Apache Airflow image as the base
FROM apache/airflow:2.10.4

# Set the working directory inside the container
WORKDIR /opt/airflow

# Copy the Python dependencies file
COPY requirements.txt ./

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy DAGs, scripts, configuration files, and plugins into the container
COPY dags/ /opt/airflow/dags/
COPY scripts/ /opt/airflow/scripts/
COPY config/ /opt/airflow/config/
COPY plugins/ /opt/airflow/plugins/

# Ensure proper file permissions
RUN chmod -R 755 /opt/airflow/

# Set the default command to start the Airflow webserver
CMD ["airflow", "webserver"]