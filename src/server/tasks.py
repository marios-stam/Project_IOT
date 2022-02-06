from .extensions import scheduler

from .bins.db_interface import get_bins_by_status


# @scheduler.task(
#     "interval",
#     id="bins_check_status",
#     seconds=10,
#     max_instances=1,
#     start_date="2000-01-01 12:19:00",
# )
# def task():
#     # Check all full bins and report them to the server
#     print("Scheduled job:Checking all bins that are going to be full")
#     with scheduler.app.app_context():
#         bins = get_bins_by_status("full")
#         print(f"Found {len(bins)} bins that are going to be full")
#     # print(bins)
