#!/usr/bin/env bash


function install(){
    get_os
    # function_calling db_name user pwd
    create_database 'expense_tracker' 'admin' 'password123'
    # sync_tables
}

function get_os(){
ubuntu_os=$(cat /proc/version | grep ubuntu | wc -l)
if [[ $ubuntu_os -gt 0 ]];then
    echo "Ubuntu Linux."
    update_repo
    install_dependencies
else
    echo "Not supported os"
    exit 1
fi

}

function update_repo(){
 apt-get update
}

function install_dependencies(){
 echo "Installing postgresql..."
 apt-get install -y libpq-dev postgresql postgresql-contrib python-pip
 apt-get install -y python-psycopg2
 echo "Installing python required packages ..."
 pip install pipenv
 pipenv install
 # pipenv shell
 if [[ $? -ne 0 ]];then
    echo "python package installtion has failed please see file"
    FCOUNT=$((FCOUNT + 1))
    exit 8
 fi
}

#Open postgres and create database with role

function __create_database__(){
    sudo -u postgres psql -c "CREATE DATABASE $1;" 
    sudo -u postgres psql -c "CREATE USER $2 WITH PASSWORD '$3';" 
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $1 TO $2;" 
    sudo -u postgres psql -c "ALTER USER $2 CREATEDB;" 
}

#Check if database name already exists else call __create_database__

function create_database(){
    echo "creating database for $1"
    db_count=`sudo -u postgres psql postgres -l | grep $1 | wc -l`
    if [[ $db_count -gt 0 ]];then
        echo "Database $1 already exists."
    else
        echo "Creating database"
        __create_database__ $1 $2 $3
    	echo "Database created successfully"
    fi
}

function sync_tables(){
    python web/manage.py makemigrations
    python web/manage.py migrate

}

#Check for EUID is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

install
