import unittest

import check
from concourse_common import testutil


class TestCheck(unittest.TestCase):
    def test_invalid_json(self):
        testutil.put_stdin(
            """
            {
               "sourcez":{
                  "access_key_id": "apiKey123",
                  "secret_access_key": "secretKey321"
               },
               "version":{
                  "schema": "version-v1-dev"
               }
            }
            """)

        self.assertEqual(check.execute(), -1)

    def test_version_not_required_json(self):
        testutil.put_stdin(
            """
            {
               "source":{
                  "access_key_id": "apiKey123",
                  "secret_access_key": "secretKey321"
               }
            }
            """)

        self.assertEqual(check.execute(), 0)

    def test_version_is_null(self):
        testutil.put_stdin(
            """
            {
               "source":{
                  "access_key_id": "apiKey123",
                  "secret_access_key": "secretKey321"
               },
               "version": null
            }
            """)

        self.assertEqual(check.execute(), 0)

    def test_version_is_empty(self):
        testutil.put_stdin(
            """
            {
               "source":{
                  "access_key_id": "apiKey123",
                  "secret_access_key": "secretKey321"
               },
               "version": {}
            }
            """)

        self.assertEqual(check.execute(), 0)

    def test_json(self):
        testutil.put_stdin(
            """
            {
               "source":{
                  "access_key_id": "apiKey123",
                  "secret_access_key": "secretKey321"
               },
               "version":{
                  "schema": "version-v1-dev"
               }
            }
            """)

        self.assertEqual(check.execute(), 0)


if __name__ == '__main__':
    unittest.main()
