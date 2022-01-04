from dagster import ScheduleDefinition
from jobs.bmi.config import bmi_local

bmi_local_schedule = ScheduleDefinition(job=bmi_local, cron_schedule="0 0 * * *")
