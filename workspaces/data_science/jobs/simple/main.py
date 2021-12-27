import time

from dagster import Boolean, Int, graph, op


def multiple_by_three(input_number: Int) -> Int:
    return input_number * 3


@op(config_schema={"sleep_time": Int})
def multiple_time(context) -> Int:
    multi_sleep_time = multiple_by_three(context.op_config["sleep_time"])
    context.log.info(f"Setting sleep time for {multi_sleep_time} seconds")
    return multi_sleep_time


@op
def sleeper(context, multi_sleep_time: Int) -> Boolean:
    context.log.info("Sleeping")
    time.sleep(multi_sleep_time)
    return True


@graph
def demo():
    multi_time = multiple_time()
    sleeper(multi_time)
