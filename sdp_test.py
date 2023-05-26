#DATETIME
from datetime import timedelta, datetime
import os

#DAG OBJECT
from airflow import DAG

# VARIABLE OBJECT
from airflow.models import Variable

#OPERATORS
from airflow.operators.bash import BashOperator

os.environ['DBT_SNOWFLAKE_ACCOUNT'] = Variable.get('DBT_SNOWFLAKE_ACCOUNT')
os.environ['DBT_SNOWFLAKE_BRONZE_PASSWORD'] = Variable.get('DBT_SNOWFLAKE_BRONZE_PASSWORD')
os.environ['DBT_SNOWFLAKE_BRONZE_USERNAME'] = Variable.get('DBT_SNOWFLAKE_BRONZE_USERNAME')

os.environ["DBT_LOG_PATH"] = "/usr/local/airflow/tmp/sdp_piano/logs"
os.environ["DBT_PACKAGE_PATH"] = "/usr/local/airflow/tmp/sdp_piano/dbt_packages"
os.environ["DBT_TARGET_PATH "] = "/usr/local/airflow/tmp/sdp_piano/target"


with DAG(
        "Test_Airflow_setup",
        default_args={
        "depends_on_past": False,
        "email": ["rajesh.ravindran@bbc.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
        },
        description="CODE TO TEST AIRFLOW SETUP",
        schedule=None, #timedelta(days=1),
        start_date=datetime(2022, 1, 1),
        catchup=False,
        tags=["TEST", "SDP-TEST"]
) as dag:
    START = BashOperator(
        task_id="START",
        bash_command="echo started"
    )

    TEST = BashOperator(
        task_id = "TEST",
        depends_on_past=False,
        # bash_command = "/usr/local/airflow/.local/bin/dbt --version",
        bash_command="cp -R /usr/local/airflow/dags/sdp_piano /tmp/sdp_piano; \
             cd /tmp/sdp_piano; \
             /usr/local/airflow/.local/bin/dbt run --project-dir /tmp/sdp_piano --profiles-dir .; \
             cat /usr/local/airflow/tmp/sdp_piano/logs/dbt.log; \
             dbt clean",
    )

    END = BashOperator(
        task_id="END",
        bash_command="echo completed"
    )

   
    START >> TEST >> END
