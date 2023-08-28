"""
Define the default arguments for all DAGs used in pipelines, 
by default all task failures will be sent to the slack channel. 
"""

from .slack import send_slack_task_failure

# Define the default airflow arguments, these will be passed
# to all tasks. This defines the use of send_slack_alert
# in the event of a task failing.

# Add
# "on_failure_callback": send_slack_task_failure,
# to this to re-enable Slack alerts
DEFAULT_ARGS = {
  "owner": "BBC",
  "depends_on_past": False,
  "email": ["data@bbc.co.uk"],
  "email_on_failure": False,
  "email_on_retry": False,
  'retries': 0
}