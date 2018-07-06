# API Rest Project of Get4me

This project is an API to the Get4me solution generated at the event Intelbras LAB.

## Requirements

This project can be executed in several operation system (SO), but has the following dependencies:
* [Django](https://www.djangoproject.com/) == 1.11.11
* [Djangorestframework](http://www.django-rest-framework.org/) == 3.8.2
* [Mysqlclient] (https://mysqlclient.readthedocs.io/) == 1.3.13
* [Python](https://www.python.org/) >= 3
* [Pip](http://www.pip-installer.org/en/latest/)

## Setup

To set up the containers, you need to execute

```
docker-compose build
```

This command will build two containers: one container for api and the another container for database

## Running

To run the containers, you need to execute

```
docker-compose up
```

This command will run the database and the API. So now, you can access the API using the follow step:
```
curl -X GET http://127.0.0.1:8000/
```

Or, you can access using your browser with the address ```http://127.0.0.1:8000/```
