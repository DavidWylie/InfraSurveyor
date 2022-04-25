import unittest
from click.testing import CliRunner
from infra_surveyor.commands import cli


class CliStructureTests(unittest.TestCase):
    """Test Suite to check command structure exists as expected"""

    def test_missing_command_fails(self):
        runner = CliRunner()
        result = runner.invoke(cli, "example")
        self.assertEqual(result.exit_code, 2, result)

    def test_survey_aws_subcommand_exists(self):
        runner = CliRunner()
        result = runner.invoke(cli, "survey-aws")
        self.assertEqual(result.exit_code, 0), result

    def test_survey_aws_events_subcommand_exists(self):
        runner = CliRunner()
        # Invoke with help option as we don't care about its execution here just its place in the hierarchy
        result = runner.invoke(cli, "survey-aws events --help")
        self.assertEqual(result.exit_code, 0, result)


if __name__ == "__main__":
    unittest.main()
