import unittest
from unittest.mock import MagicMock, patch

import out
from concourse_common import testutil
from eb_deployer import Eb_deployer


class TestOut(unittest.TestCase):
    def setUp(self):
        Eb_deployer.execute_command = MagicMock(name='execute_command')

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
        Eb_deployer.execute_command.return_value = 0

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

    def test_deploy(self):
        Eb_deployer.execute_command.return_value = 0

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
                "artifact_file": "artifact/package.zip",
                "config_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        Eb_deployer.execute_command.assert_called_with(['eb_deploy', '-c', r'/tmp/put/source/ci/eb_deployer.yml',
                                                        '-p', r'/tmp/put/artifact/package.zip',
                                                        '-e', 'dev'],
                                                       r'/tmp/put/')

    @patch("io.open")
    def test_deploy_with_stage_file(self, mock_io_open):
        Eb_deployer.execute_command.return_value = 0
        mock_file = MagicMock()
        mock_io_open.return_value = mock_file
        mock_file.read.return_value = "dev"

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
                "artifact_file": "artifact/package.zip",
                "config_file": "source/ci/"
              }
            }
            """)

        self.assertEqual(out.execute(r'/tmp/put/'), 0)
        Eb_deployer.execute_command.assert_called_with(['eb_deploy', '-c', r'/tmp/put/source/ci/eb_deployer.yml',
                                                        '-p', r'/tmp/put/artifact/package.zip',
                                                        '-e', 'dev'],
                                                       r'/tmp/put/')

    def test_remove(self):
        Eb_deployer.execute_command.return_value = 0

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
        Eb_deployer.execute_command.assert_called_with(['eb_deploy',
                                                        '-c', r'/tmp/put/source/ci/eb_deployer.yml',
                                                        '-e', 'dev', '-d'],
                                                       r'/tmp/put/')

    @patch("io.open")
    def test_remove_with_stage_file(self, mock_io_open):
        Eb_deployer.execute_command.return_value = 0
        mock_file = MagicMock()
        mock_io_open.return_value = mock_file
        mock_file.read.return_value = "dev"

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
        Eb_deployer.execute_command.assert_called_with(['eb_deploy',
                                                        '-c', r'/tmp/put/source/ci/eb_deployer.yml',
                                                        '-e', 'dev', '-d'],
                                                       r'/tmp/put/')


if __name__ == '__main__':
    unittest.main()
