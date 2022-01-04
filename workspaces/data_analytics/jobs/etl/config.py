from dagster import ResourceDefinition
from jobs.etl.main import etl
from jobs.etl.resource import postgres_resource

local = {"ops": {"create_table": {"config": {"table_name": "fake_table"}}}}

docker = {
    "resources": {
        "database": {
            "config": {
                "host": "postgresql",
                "user": "postgres_user",
                "password": "postgres_password",
                "database": "postgres_db",
            }
        }
    },
    "ops": {"create_table": {"config": {"table_name": "postgres_table"}}},
}

etl_local = etl.to_job(
    name="etl_local",
    config=local,
    resource_defs={"database": ResourceDefinition.mock_resource()},
    tags={"Demo": True},
)

etl_docker = etl.to_job(
    name="etl_docker",
    config=docker,
    resource_defs={"database": postgres_resource},
    tags={"Demo": True},
)
