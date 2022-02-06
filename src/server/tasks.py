from datetime import datetime

from flask_apscheduler import APScheduler

scheduler = APScheduler()


@scheduler.task(
    "interval",
    id="bins_check_status",
    seconds=20,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def task1():
    """Sample task 1.
    Added when app starts.
    """
    print("running task 1!")  # noqa: T001
