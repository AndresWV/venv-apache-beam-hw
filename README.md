# Airflow demo

For the purposes of this demo I will be using Ubuntu 20.20 and Python 3.8.8. 
Airflow does not work on Windows currently. 

## 0. Setup and enter a virtual environment  
execute in shell 1 and 2
```shell
python -m venv venv
source venv/bin/activate
```

## 1. Set `AIRFLOW_HOME`
execute in shell 1 and 2
```shell
export AIRFLOW_HOME=`pwd`/airflow
```

### 1.1 (Optional) Set `AIRFLOW__CORE__LOAD_EXAMPLES` to false 

```shell
export AIRFLOW__CORE__LOAD_EXAMPLES=false
```

## 2. Install Airflow

```shell
pip install apache-airflow
```

## 3. Initialise database with an user

```shell
airflow db init

airflow users create \
    --username Airflow \
    --firstname Airflow \
    --lastname Airflow \
    --role Admin \
    --password airflow \
    --email airflow@gmail.com
```

## 4. Start the services 

Use two different terminals, remember to activate your Python environment and set the environment variables!

### 4.1 Start the web server

```shell
airflow webserver --port 8080
```

### 4.2 Start the web server

```shell
airflow scheduler
```

## 5. Add a dags folder   

Inside the `$AIRFLOW_HOME` folder  

```shell
mkdir $AIRFLOW_HOME/dags
```

## 6. Add your first DAG

Create a file `first.py` in the newly created folder

### 6.1 Add imports

```python
from datetime import timedelta

from airflow import DAG

from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import logging
```

### 6.2 Add a `default_args` dictionary

These values are passed by default into each task, they may be overriden on an individual basis for each task.

```python
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
```

### 6.3 Create some Python functions 

These are the actions we will call for our DAG

```python
def scrape():
    logging.info("performing scraping")

def process():
    logging.info("performing processing")

def save():
    logging.info("performing saving")
```

### 6.4 Define the DAG

Finally, define our DAG and its tasks

```python
with DAG(
    'first',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    scrape_task = PythonOperator(task_id="scrape", python_callable=scrape)
    process_task = PythonOperator(task_id="process", python_callable=process)
    save_task = PythonOperator(task_id="save", python_callable=save)
```

### 6.5 Specify dependencies between tasks

```python
    scrape_task >> process_task >> save_task
```

