import boto3
from dagster import RunRequest, SkipReason, sensor
from jobs.bmi.config import bmi_local


def get_s3_keys(
    bucket: str,
    prefix: str = "",
    endpoint_url: str = None,
    since_key: str = None,
    max_keys: int = 1000,
):
    """Get S3 keys"""
    config = {"service_name": "s3"}
    if endpoint_url:
        config["endpoint_url"] = endpoint_url

    client = boto3.client(**config)

    cursor = ""
    contents = []

    while True:
        response = client.list_objects_v2(
            Bucket=bucket,
            Delimiter="",
            MaxKeys=max_keys,
            Prefix=prefix,
            StartAfter=cursor,
        )
        contents.extend(response.get("Contents", []))
        if response["KeyCount"] < max_keys:
            break

        cursor = response["Contents"][-1]["Key"]

    sorted_keys = [
        obj["Key"] for obj in sorted(contents, key=lambda x: x["LastModified"])
    ]

    if not since_key or since_key not in sorted_keys:
        return sorted_keys

    for idx, key in enumerate(sorted_keys):
        if key == since_key:
            return sorted_keys[idx + 1 :]

    return []


@sensor(job=bmi_local, minimum_interval_seconds=30)
def bmi_local_s3_sensor(context):
    new_s3_keys = get_s3_keys(
        bucket="dagster",
        prefix="sensor",
        endpoint_url="http://host.docker.internal:4566",
    )
    if not new_s3_keys:
        yield SkipReason("No new s3 files found for bucket my_s3_bucket.")
        return
    for s3_key in new_s3_keys:
        yield RunRequest(
            run_key=s3_key,
            run_config={
                "ops": {
                    "pounds_to_kilograms": {"config": {"weight_pounds": 190}},
                    "inches_to_meters": {"config": {"height_inches": 75}},
                },
            },
        )
