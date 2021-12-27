from dagster import Float, Int, graph, op


@op(config_schema={"weight_pounds": Int})
def pounds_to_kilograms(context) -> Float:
    return context.op_config["weight_pounds"] / 2.2046


@op(config_schema={"height_inches": Int})
def inches_to_meters(context) -> Float:
    return context.op_config["height_inches"] * 0.0254


@op
def calcualte_bmi(context, weight_kilograms: Float, height_meters: Float) -> Float:
    bmi = weight_kilograms / height_meters ** 2
    context.log.info(f"BMI: {bmi}")
    return bmi


@op
def bmi_weight(context, bmi: Float):
    if bmi < 18.5:
        context.log.info(f"Underweight")
    elif 18.5 <= bmi < 25:
        context.log.info(f"Healthy")
    elif 25 <= bmi < 30:
        context.log.info(f"Overweight")
    else:
        context.log.info(f"Obese")


@graph
def bmi():
    kilograms = pounds_to_kilograms()
    meters = inches_to_meters()
    bmi = calcualte_bmi(kilograms, meters)
    bmi_weight(bmi)
