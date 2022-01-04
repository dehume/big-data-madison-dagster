from dagster import repository
from jobs.bmi.config import bmi_local
from jobs.bmi.schedules import bmi_local_schedule
from jobs.bmi.sensors import bmi_local_s3_sensor
from jobs.etl.config import etl_local, etl_docker

JOBS = [etl_local, etl_docker, bmi_local]
SCHEDULES = [bmi_local_schedule]
SENSORS = [bmi_local_s3_sensor]


@repository
def repo():
    return JOBS + SCHEDULES + SENSORS
