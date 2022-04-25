from unittest import TestCase
from unittest.mock import Mock, patch
from click.testing import CliRunner
from infra_surveyor.commands import cli
from infra_surveyor.cloud.models import Resource, Link
from infra_surveyor.graphing import Graph
import os


class TestCommands(TestCase):
    DEFAULT_DIR = "."
    DEFAULT_FILE_NAME = "aws-events"
    DEFAULT_EXT = "png"

    def _create_test_nodes(self):
        test_dir = os.path.dirname(__file__)
        image_1 = (
            f"{test_dir}/../"
            "src/"
            "infra_surveyor_aws_icons/"
            "Resource-Icons_01312022/"
            "Res_Quantum-Technologies/Res_48_Light/"
            "Res_Amazon-Braket_QPU _48_Light.svg"
        )
        nodes = [
            Resource(
                name="First",
                resource_type="Aws-Lambda",
                id="test-1-arn",
                service="test",
                category="test",
                image=image_1,
            ),
            Resource(
                name="Second",
                resource_type="Aws-Lambda",
                id="test-2-arn",
                service="test",
                category="test",
                image=image_1,
            ),
            Resource(
                name="Third",
                resource_type="Aws-Lambda",
                id="test-3-arn",
                service="test",
                category="test",
                image=image_1,
            ),
            Resource(
                name="Forth",
                resource_type="Aws-Lambda",
                id="test-4-arn",
                service="test",
                category="test",
            ),
            Resource(
                name="Fifth",
                resource_type="Aws-Lambda",
                id="test-5-arn",
                service="test",
                category="test",
            ),
        ]
        return nodes

    def _create_test_links(self):
        links = [
            Link("test-1-arn", "test-2-arn", "testing"),
            Link("test-1-arn", "test-3-arn", "testing"),
            Link("test-1-arn", "test-4-arn", "testing"),
            Link("test-1-arn", "test-5-arn", "testing"),
        ]
        return links

    @patch("infra_surveyor.cloud.aws.survey_events")
    @patch("infra_surveyor.graphing.create_graph")
    @patch("infra_surveyor.icons.load_icons")
    def test_survey_aws_event_defaults(
        self, mock_load_icons, mock_create_graph: Mock, mock_survey: Mock
    ):
        runner = CliRunner()
        nodes = self._create_test_nodes()
        links = self._create_test_links()

        mock_survey.return_value = (nodes, links)
        mocked_graph = Mock(Graph)
        mock_create_graph.return_value = mocked_graph

        result = runner.invoke(cli, "survey-aws events")
        self.assertEqual(result.exit_code, 0, result)
        self.assertEqual(1, mock_survey.call_count)
        self.assertEqual(1, mock_create_graph.call_count)
        self.assertEqual(1, mock_load_icons.call_count)
        self.assertEqual(
            self.DEFAULT_FILE_NAME, mocked_graph.render_graph.call_args[0][0]
        )
        self.assertEqual(self.DEFAULT_DIR, mocked_graph.render_graph.call_args[0][1])
        self.assertEqual(self.DEFAULT_EXT, mocked_graph.render_graph.call_args[0][2])

    @patch("infra_surveyor.cloud.aws.survey_events")
    @patch("infra_surveyor.graphing.create_graph")
    @patch("infra_surveyor.icons.load_icons")
    def test_survey_aws_events_custom_file_name_short(
        self, mock_load_icons, mock_create_graph: Mock, mock_survey: Mock
    ):
        runner = CliRunner()
        nodes = self._create_test_nodes()
        links = self._create_test_links()

        mock_survey.return_value = (nodes, links)
        mocked_graph = Mock(Graph)
        mock_create_graph.return_value = mocked_graph

        out_file = "output-file-name"
        result = runner.invoke(cli, f"survey-aws events -f {out_file}")
        self.assertEqual(result.exit_code, 0, result)
        self.assertEqual(1, mock_survey.call_count)
        self.assertEqual(1, mock_create_graph.call_count)
        self.assertEqual(1, mock_load_icons.call_count)
        self.assertEqual(out_file, mocked_graph.render_graph.call_args[0][0])
        self.assertEqual(self.DEFAULT_DIR, mocked_graph.render_graph.call_args[0][1])
        self.assertEqual(self.DEFAULT_EXT, mocked_graph.render_graph.call_args[0][2])

    @patch("infra_surveyor.cloud.aws.survey_events")
    @patch("infra_surveyor.graphing.create_graph")
    @patch("infra_surveyor.icons.load_icons")
    def test_survey_aws_events_custom_file_name_option(
        self, mock_load_icons, mock_create_graph: Mock, mock_survey: Mock
    ):
        runner = CliRunner()
        nodes = self._create_test_nodes()
        links = self._create_test_links()

        mock_survey.return_value = (nodes, links)
        mocked_graph = Mock(Graph)
        mock_create_graph.return_value = mocked_graph

        out_file = "output-file-name"
        result = runner.invoke(cli, f"survey-aws events --out_file {out_file}")
        self.assertEqual(result.exit_code, 0, result)
        self.assertEqual(1, mock_survey.call_count)
        self.assertEqual(1, mock_create_graph.call_count)
        self.assertEqual(1, mock_load_icons.call_count)
        self.assertEqual(out_file, mocked_graph.render_graph.call_args[0][0])
        self.assertEqual(self.DEFAULT_DIR, mocked_graph.render_graph.call_args[0][1])
        self.assertEqual(self.DEFAULT_EXT, mocked_graph.render_graph.call_args[0][2])

    @patch("infra_surveyor.cloud.aws.survey_events")
    @patch("infra_surveyor.graphing.create_graph")
    @patch("infra_surveyor.icons.load_icons")
    def test_survey_aws_events_custom_ext_svg(
        self, mock_load_icons, mock_create_graph: Mock, mock_survey: Mock
    ):
        runner = CliRunner()
        nodes = self._create_test_nodes()
        links = self._create_test_links()

        mock_survey.return_value = (nodes, links)
        mocked_graph = Mock(Graph)
        mock_create_graph.return_value = mocked_graph

        out_ext = "svg"
        result = runner.invoke(cli, f"survey-aws events --out_ext {out_ext}")
        self.assertEqual(result.exit_code, 0, result)
        self.assertEqual(1, mock_survey.call_count)
        self.assertEqual(1, mock_create_graph.call_count)
        self.assertEqual(1, mock_load_icons.call_count)
        self.assertEqual(
            self.DEFAULT_FILE_NAME, mocked_graph.render_graph.call_args[0][0]
        )
        self.assertEqual(self.DEFAULT_DIR, mocked_graph.render_graph.call_args[0][1])
        self.assertEqual("svg", mocked_graph.render_graph.call_args[0][2])

    @patch("infra_surveyor.cloud.aws.survey_events")
    @patch("infra_surveyor.graphing.create_graph")
    @patch("infra_surveyor.icons.load_icons")
    def test_survey_aws_events_custom_output_dir_option(
        self, mock_load_icons, mock_create_graph: Mock, mock_survey: Mock
    ):
        runner = CliRunner()
        nodes = self._create_test_nodes()
        links = self._create_test_links()

        mock_survey.return_value = (nodes, links)
        mocked_graph = Mock(Graph)
        mock_create_graph.return_value = mocked_graph

        out_dir = "output-dir"
        result = runner.invoke(cli, f"survey-aws events --out_dir {out_dir}")
        self.assertEqual(result.exit_code, 0, result)
        self.assertEqual(1, mock_survey.call_count)
        self.assertEqual(1, mock_create_graph.call_count)
        self.assertEqual(1, mock_load_icons.call_count)

        self.assertEqual(
            self.DEFAULT_FILE_NAME, mocked_graph.render_graph.call_args[0][0]
        )
        self.assertEqual(out_dir, mocked_graph.render_graph.call_args[0][1])
        self.assertEqual(self.DEFAULT_EXT, mocked_graph.render_graph.call_args[0][2])

    @patch("infra_surveyor.cloud.aws.survey_events")
    @patch("infra_surveyor.graphing.create_graph")
    @patch("infra_surveyor.icons.load_icons")
    def test_survey_aws_events_custom_output_dir_short(
        self, mock_load_icons, mock_create_graph: Mock, mock_survey: Mock
    ):
        runner = CliRunner()
        nodes = self._create_test_nodes()
        links = self._create_test_links()

        mock_survey.return_value = (nodes, links)
        mocked_graph = Mock(Graph)
        mock_create_graph.return_value = mocked_graph

        out_dir = "output-dir"
        result = runner.invoke(cli, f"survey-aws events -o {out_dir}")
        self.assertEqual(result.exit_code, 0, result)
        self.assertEqual(1, mock_survey.call_count)
        self.assertEqual(1, mock_create_graph.call_count)
        self.assertEqual(1, mock_load_icons.call_count)

        self.assertEqual(
            self.DEFAULT_FILE_NAME, mocked_graph.render_graph.call_args[0][0]
        )
        self.assertEqual(out_dir, mocked_graph.render_graph.call_args[0][1])
        self.assertEqual(self.DEFAULT_EXT, mocked_graph.render_graph.call_args[0][2])
