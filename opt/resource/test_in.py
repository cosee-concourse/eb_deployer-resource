import unittest
from io import TextIOWrapper
from unittest.mock import MagicMock, patch

import in_
from concourse_common import testutil


class TestInput(unittest.TestCase):

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

        self.assertEqual(in_.execute('/'), -1)

    def test_json(self):
        with patch("builtins.open", create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=TextIOWrapper)

            testutil.put_stdin(
                """
                {
                  "source": {
                    "access_key_id": "apiKey123",
                    "secret_access_key": "secretKey321"
                  },
                  "version": {
                    "env": "dev"
                  }
                }
                """)

            self.assertEqual(in_.execute('/'), 0)
            file_handle = mock_open.return_value.__enter__.return_value
            file_handle.write.assert_called_with('dev')
