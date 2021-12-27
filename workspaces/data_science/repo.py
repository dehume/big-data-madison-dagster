from dagster import repository
from jobs.simple.config import demo_local

JOBS = [demo_local]


@repository
def repo():
    return JOBS
