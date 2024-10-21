FROM apache/airflow:latest

USER root

# Installation de netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Création des répertoires nécessaires
RUN mkdir -p /opt/airflow/custom_postgres && chown -R airflow:root /opt/airflow/custom_postgres
RUN mkdir -p /home/airflow/.dbt && chown -R airflow:root /home/airflow/.dbt

# Passer à l'utilisateur airflow pour l'installation de dbt-postgres
USER airflow

# Installation de dbt-postgres et apache-airflow-providers-docker
RUN pip install --no-cache-dir dbt-core==1.8.7 dbt-postgres==1.8.2 apache-airflow-providers-docker

# Revenir à l'utilisateur root pour copier le script d'entrée
USER root
COPY --chown=airflow:root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Repasser à l'utilisateur airflow pour l'exécution
USER airflow

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]