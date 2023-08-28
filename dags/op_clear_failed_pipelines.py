from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

from utils.default_args import DEFAULT_ARGS

# Rerun at 9, 13 and 18 daily to check for failed dags
EXECUTION_SCHEDULE = "0 18 * * *"

with DAG(
    "op_clear_failed_pipelines",
    start_date=datetime(2023, 1, 1),
    max_active_runs=1,
    default_args=DEFAULT_ARGS,
    dagrun_timeout=timedelta(hours=1),
    schedule_interval=EXECUTION_SCHEDULE,
    catchup=False,
    tags=["operations"],
) as dag:
    """This DAG does the following:
    1. Clears all failed runs of the pipeline_* dags
    """
    
    clear_runs = BashOperator(
        task_id="clear_failed_runs",
        bash_command=f"airflow tasks clear --dag-regex pipeline_* --only-failed --upstream --yes ",
    )

    clear_runs