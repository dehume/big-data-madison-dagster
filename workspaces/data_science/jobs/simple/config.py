from jobs.simple.main import demo

local = {"ops": {"multiple_time": {"config": {"sleep_time": 0}}}}

demo_local = demo.to_job(config=local, tags={"Demo": True})
