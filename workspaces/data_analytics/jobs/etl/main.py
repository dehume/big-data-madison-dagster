from random import randint

from dagster import AssetMaterialization, Output, String, graph, op


@op(config_schema={"table_name": String}, required_resource_keys={"database"})
def create_table(context) -> String:
    table_name = context.op_config["table_name"]
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} (column_1 VARCHAR(100));"
    context.resources.database.execute_query(sql)
    return table_name


@op(required_resource_keys={"database"})
def insert_into_table(context, table_name: String):
    sql = f"INSERT INTO {table_name} (column_1) VALUES (1);"

    number_of_rows = randint(1, 10)
    for _ in range(number_of_rows):
        context.resources.database.execute_query(sql)
        context.log.info("Inserted a row")

    context.log.info("Batch inserted")

    yield AssetMaterialization(
        asset_key="my_micro_batch",
        description="Inserting a random batch of records",
        metadata={"table_name": table_name, "number_of_rows": number_of_rows},
    )
    yield Output(number_of_rows)


@graph
def etl():
    table = create_table()
    insert_into_table(table)
