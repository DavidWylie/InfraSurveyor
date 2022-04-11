import unittest
from click.testing import CliRunner
from surveyor.main import cli


class CliStructureTests(unittest.TestCase):
    """Test Suite to check command structure exists as expected"""
    def test_missing_command_fails(self):
        runner = CliRunner()
        result = runner.invoke(cli, "example")
        self.assertTrue(result.exit_code, 2)

    def test_survey_aws_subcommand_exists(self):
        runner = CliRunner()
        result = runner.invoke(cli, "survey-aws")
        self.assertTrue( result.exit_code == 0)

    def test_survey_aws_events_subcommand_exists(self):
        runner = CliRunner()
        result = runner.invoke(cli, "survey-aws events")
        self.assertTrue(result.exit_code == 0)


if __name__ == "__main__":
    unittest.main()
