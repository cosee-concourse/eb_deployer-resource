import unittest
from unittest.mock import MagicMock, patch

import out
from concourse_common import testutil
from eb_deployer import EBDeployer


class TestOut(unittest.TestCase):
    def setUp(self):
        EBDeployer.execute_command = MagicMock(name='execute_command')

    def test_invalid_json(self):
        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    def test_params_required_json(self):
        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    def test_deploy_artifact_file_needed(self):
        EBDeployer.execute_command.return_value = 0

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "env": "dev",
                "deploy": true,
                "config_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute('/'), -1)

    @patch("eb_deployer.files")
    @patch("eb_deployer.validate_path")
    def test_deploy(self, mock_validate_path, mock_files):
        mock_validate_path.return_value = True
        mock_files.return_value = ['package-1.0.0.zip', 'foo.txt', 'bar.zip', 'package-1.0.0.jar']
        EBDeployer.execute_command.return_value = 0

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "env": "dev",
                "deploy": true,
                "artifact_file": "artifact/package-(.*).zip",
                "config_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        EBDeployer.execute_command.assert_called_with(['eb_deploy',
                                                        '-p', r'/tmp/put/artifact/package-1.0.0.zip',
                                                        '-e', 'dev'],
                                                       r'/tmp/put/source/ci/')

    @patch("eb_deployer.files")
    @patch("eb_deployer.validate_path")
    @patch("out.ioutil")
    def test_deploy_with_stage_file(self, mock_ioutil, mock_validate_path, mock_files):
        EBDeployer.execute_command.return_value = 0
        mock_validate_path.return_value = True
        mock_ioutil.read_file.return_value = "dev"
        mock_files.return_value = ['package-1.0.0.zip', 'foo.txt', 'bar.zip', 'package-1.0.0.jar']


        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "env_file": "naming/env",
                "deploy": true,
                "artifact_file": "artifact/package-(.*).zip",
                "config_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        EBDeployer.execute_command.assert_called_with(['eb_deploy',
                                                        '-p', r'/tmp/put/artifact/package-1.0.0.zip',
                                                        '-e', 'dev'],
                                                       r'/tmp/put/source/ci/')

    @patch("eb_deployer.validate_path")
    def test_remove(self, mock_validate_path):
        EBDeployer.execute_command.return_value = 0
        mock_validate_path.return_value = True

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "env": "dev",
                "remove": true,
                "config_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        EBDeployer.execute_command.assert_called_with(['eb_deploy',
                                                        '-e', 'dev', '-d'],
                                                       r'/tmp/put/source/ci/')

    @patch("eb_deployer.validate_path")
    @patch("out.ioutil")
    def test_remove_with_stage_file(self, mock_ioutil, mock_validate_path):
        EBDeployer.execute_command.return_value = 0
        mock_ioutil.read_file.return_value = "dev"
        mock_validate_path.return_value = True

        testutil.put_stdin(
            """
            {
              "source": {
                "access_key_id": "apiKey123",
                "secret_access_key": "secretKey321"
              },
              "params": {
                "env_file": "release",
                "remove": true,
                "config_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        EBDeployer.execute_command.assert_called_with(['eb_deploy',
                                                        '-e', 'dev', '-d'],
                                                       r'/tmp/put/source/ci/')


if __name__ == '__main__':
    unittest.main()
