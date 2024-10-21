# ELT Data Pipeline Project

## Overview

This project demonstrates a comprehensive Extract, Load, and Transform (ELT) data pipeline using modern data engineering tools and practices. It showcases the integration of PostgreSQL, Apache Airflow, dbt (data build tool), and Docker to create a robust, scalable, and automated data workflow.

## Key Technologies

- **PostgreSQL**: Used for both source and destination databases
- **Apache Airflow**: Orchestrates the entire ELT process
- **dbt (data build tool)**: Handles data transformations
- **Docker & Docker Compose**: Ensures consistent environments and easy deployment
- **Python**: Powers custom scripts for data extraction and loading

## Project Structure

.
├── airflow/
│   ├── airflow.cfg
│   └── dags/
│       └── elt_dag.py
├── custom_postgres/
│   ├── dbt_project.yml
│   └── models/
├── elt_script/
│   └── elt_script.py
├── logs/
├── source_db_init/
├── dbt_profiles.yml
├── docker-compose.yaml
├── Dockerfile
├── entrypoint.sh
└── README.md


## Pipeline Overview

1. **Extraction**: Data is extracted from a source PostgreSQL database using a custom Python script.
2. **Loading**: The extracted data is loaded into a destination PostgreSQL database.
3. **Transformation**: Data in the destination database is transformed using dbt models.
4. **Orchestration**: The entire process is orchestrated by Apache Airflow, ensuring reliable and scheduled execution.

## Key Features

- **End-to-End Automation**: The entire ELT process is automated and orchestrated using Apache Airflow.
- **Data Transformation**: Utilizes dbt for writing, documenting, and executing data transformations.
- **Containerization**: The entire solution is containerized using Docker, ensuring consistency across environments.
- **Scalability**: The architecture is designed to handle increasing data volumes and complexity.
- **Modularity**: Each component (extraction, loading, transformation) is separate, allowing for easy modifications and extensions.

## Setup and Execution

1. Clone the repository:
   git clone https://github.com/your-username/elt-data-pipeline.git
   cd elt-data-pipeline
2. Start the services: 
  docker-compose up -d
3. Access Airflow web interface:
  http://localhost:8083
4. Trigger the `elt_and_dbt` DAG in Airflow to run the pipeline
   
## Learning Outcomes

This project demonstrates proficiency in:

- Designing and implementing ELT pipelines
- Working with containerized applications using Docker
- Orchestrating complex workflows with Apache Airflow
- Data transformation using SQL and dbt
- Database management with PostgreSQL
- Python scripting for data manipulation
