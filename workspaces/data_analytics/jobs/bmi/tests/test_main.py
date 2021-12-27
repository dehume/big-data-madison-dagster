import unittest

from dagster import ExecuteInProcessResult, build_op_context
from jobs.bmi.config import bmi_local
from jobs.bmi.main import (bmi_weight, calcualte_bmi, inches_to_meters,
                           pounds_to_kilograms)


class TestBMIJob(unittest.TestCase):
    """Test BMI job"""

    def test_pounds_to_kilograms(self):
        """Test pounds_to_kilograms"""
        with build_op_context(op_config={"weight_pounds": 100}) as context:
            result = pounds_to_kilograms(context)
            self.assertEqual(result, 45.35970244035199)

    def test_inches_to_meters(self):
        """Test inches_to_meters"""
        with build_op_context(op_config={"height_inches": 72}) as context:
            result = inches_to_meters(context)
            self.assertEqual(result, 1.8288)

    def test_calcualte_bmi(self):
        """Test calcualte_bmi"""
        with build_op_context() as context:
            result = calcualte_bmi(context, 89.0, 72.0)
            self.assertEqual(result, 0.01716820987654321)

    def test_bmi_weight(self):
        """Test bmi_weight"""
        with build_op_context() as context:
            bmi_weight(context, 22.12)

    def test_job_run(self):
        """Test job"""
        result = bmi_local.execute_in_process()
        assert isinstance(result, ExecuteInProcessResult)
        assert result.success
