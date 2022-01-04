import unittest

from dagster import ExecuteInProcessResult, build_op_context
from jobs.simple.config import demo_local
from jobs.simple.main import multiple_by_three, multiple_time, sleeper


class TestDemoJob(unittest.TestCase):
    """Test demo job"""

    def test_multiple_by_three(self):
        """Test multiple_by_three function"""
        result = multiple_by_three(3)
        self.assertEqual(result, 9)

        result = multiple_by_three(6)
        self.assertEqual(result, 18)

    def test_multiple_time(self):
        """Test multiple time op"""
        with build_op_context(op_config={"sleep_time": 5}) as context:
            result = multiple_time(context)
            self.assertEqual(result, 15)

    def test_sleeper(self):
        """Test sleeper"""
        with build_op_context() as context:
            result = sleeper(context, 0)
            self.assertTrue(result)

    def test_job_run(self):
        """Test job"""
        result = demo_local.execute_in_process()
        assert isinstance(result, ExecuteInProcessResult)
        assert result.success
