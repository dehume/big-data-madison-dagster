import sqlalchemy
from dagster import Field, Int, String, resource


class Postgres:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._engine = sqlalchemy.create_engine(self.uri)

    @property
    def uri(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}/{self.database}"

    def execute_query(self, query: str):
        self._engine.execute(query)


@resource(
    config_schema={
        "host": Field(String),
        "user": Field(String),
        "password": Field(String),
        "database": Field(String),
    },
    description="A resource that can run Postgres",
)
def postgres_resource(context) -> Postgres:
    """This resource defines a Mongo client"""
    return Postgres(
        host=context.resource_config["host"],
        user=context.resource_config["user"],
        password=context.resource_config["password"],
        database=context.resource_config["database"],
    )
