from dagster import String, graph, op


@op(required_resources_keys={"database"}, config_schema={"table_name": String})
def create_table(context) -> String:
    table_name = context.op_config["table_name"]
    sql = f"CREATE TABLE {table_name} (column_1 VARCHAR(100));"
    context.resources.database.execute_query(sql)
    return table_name


@op(required_resources_keys={"database"}, config_schema={"table_name": String})
def insert_into_table(context, table_name: String):
    sql = f"INSERT INTO {table_name} (column_1) VALUES (1);"
    context.resources.database.execute_query(sql)


@graph
def etl():
    table = create_table()
    insert_into_table(table)
