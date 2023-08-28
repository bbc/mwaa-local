"""
Utility script for sending notifications to Slack from Airflow
"""

from airflow import configuration
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

# Slack alerts for failing tasks:
def send_slack_alert(context, **kwargs):
    """
    Given an Airflow context, send a slack alert to the Slack webhook
    stored in airflow/connections/slack_webhook_url in AWS secrets vault.

    Args:
        context: The Airflow job context, including key information to log
        message (str): Slack message body
        blocks (list): Slack message blocks
        attachments (list): Slack message attachments
        **kwargs: Arbitrary keyword arguments

    Returns:
        The result of executing the SlackWebhookOperator
    """

    # Create a SlackWebHook, pass the message and set the username
    # to be airflow.
    slack_alert = SlackWebhookOperator(
        task_id="slack_alert",
        http_conn_id="slack_webhook_url",
        username="Airflow",
        **kwargs,
    )

    # Send the message and return the result
    return slack_alert.execute(context=context)


def send_slack_task_failure(context):
    """
    Send a failure notification to the relevant slack channel including
    task and dag information

    Args:
        context: The Airflow job context, including key information to log
    
    Returns:
        The result of executing send_slack_alert
    """
    # Get the DAG object of the failed pipeline
    dag = context.get("dag")
    # Get the task object for the failed pipeline
    task = context.get("task_instance")
    # Get the date of execution
    execution_date = context.get("ds")
    execution_timestamp = context.get("ts")

    # Add a link to the airflow instance as a button
    # Get the current airflow URL
    airflow_url = configuration.get("webserver", "BASE_URL")
    dag_url = f"https://{airflow_url}/admin/airflow/log?dag_id={dag.dag_id}"
    emr_url = "https://eu-west-1.console.aws.amazon.com/elasticmapreduce/home?region=eu-west-1#"

    # Create a block formatted message
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"⚠️ Airflow task failure {execution_date}",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Pipeline:*\n{dag.dag_id}",
                },
                {"type": "mrkdwn", "text": f"*Task:*\n{task.task_id}"},
            ],
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Open EMR", "emoji": True},
                    "url": emr_url,
                },
            ],
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": f"Execution Timestamp: {execution_timestamp}",
                    "emoji": True,
                }
            ],
        },
    ]

    send_slack_alert(
        context, message=f"Failure of {task.task_id} on {dag.dag_id}", blocks=blocks
    )