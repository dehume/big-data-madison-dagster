from jobs.bmi.main import bmi

local = {
    "ops": {
        "pounds_to_kilograms": {"config": {"weight_pounds": 190}},
        "inches_to_meters": {"config": {"height_inches": 75}},
    },
}

bmi_local = bmi.to_job(config=local, tags={"Demo": True})
