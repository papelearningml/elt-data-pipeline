#!/bin/bash
set -e

# Vérifier si Airflow est correctement installé
if ! command -v airflow &> /dev/null; then
    echo "Erreur : Airflow n'est pas installé ou n'est pas dans le PATH"
    exit 1
fi

# Attendre que la base de données soit disponible
echo "Attente de la disponibilité de la base de données..."
while ! nc -z postgres 5432; do
    sleep 1
done
echo "Base de données disponible."

# Initialiser la base de données Airflow si nécessaire
airflow db init

# Créer un utilisateur admin si nécessaire
if ! airflow users list | grep -q 'admin'; then
    echo "Création de l'utilisateur admin..."
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin
fi

# Démarrer le service (webserver ou scheduler)
echo "Démarrage du service Airflow : $@"
exec airflow "$@"