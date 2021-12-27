from jobs.etl.main import etl

local = {}

docker = {}

etl_local = etl.to_job(config=local, tags={"Demo": True})

etl_docker = etl.to_job(config=docker, tags={"Demo": True})
