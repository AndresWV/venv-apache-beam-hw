from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

# Definición de las etiquetas para el DAG
TAGS = ['example']

# Definición de parámetros del DAG
DAG_ID = 'hello'
DAG_DESCRIPTION = 'Mi primer DAG en Airflow'
DAG_SCHEDULE = timedelta(days=1) # Programación del DAG 

# Argumentos por defecto para las tareas del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Configuración de reintentos y retraso entre reintentos
retries = 4
retry_delay = timedelta(minutes=5)

# Función que se ejecutará en la tarea de Python
def execute_task(**kwargs):
    print("Hola Mundo")

# Creación del DAG con sus propiedades
dag = DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description=DAG_DESCRIPTION,
    schedule_interval=DAG_SCHEDULE,
    start_date=days_ago(2),
    tags=TAGS
)

# Definición de las tareas asociadas al DAG dentro de un contexto 'with'
with dag as dag:
    # Tarea de inicio del proceso
    start_task = EmptyOperator(task_id='inicia_proceso')
    
    # Tarea de finalización del proceso
    end_task = EmptyOperator(task_id='finaliza_proceso')
    
    # Tarea que ejecuta una función de Python
    first_task = PythonOperator(
        task_id='first_task',
        python_callable=execute_task,
        retries=retries,
        retry_delay=retry_delay
    )

    # Establecimiento de la dependencia entre las tareas
    start_task >> first_task >> end_task
