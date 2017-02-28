import unittest

from concourse_common import testutil

from model import Model, Request
import payloads


class TestModel(unittest.TestCase):
    def setUpGetterTest(self, payload, request):
        testutil.put_stdin(payload)
        self.model = Model(request)

    def test_get_access_key(self):
        self.setUpGetterTest(payloads.check_payload, Request.CHECK)
        api_key = self.model.get_access_key()
        self.assertEqual(api_key, "apiKey123")

    def test_get_secret_key(self):
        self.setUpGetterTest(payloads.check_payload, Request.CHECK)
        secret_key = self.model.get_secret()
        self.assertEqual(secret_key, "secretKey321")

    def test_get_env_version(self):
        self.setUpGetterTest(payloads.check_payload, Request.CHECK)
        version = self.model.get_env_version()
        self.assertEqual(version, "dev")

    def test_get_config_file(self):
        self.setUpGetterTest(payloads.out_deploy_payload, Request.OUT)
        version = self.model.get_config_file()
        self.assertEqual(version, "source/ci/eb_deployer.yml")

    def test_get_artifact_file(self):
        self.setUpGetterTest(payloads.out_deploy_payload, Request.OUT)
        version = self.model.get_artifact_file()
        self.assertEqual(version, "artifact/package.zip")


if __name__ == '__main__':
    unittest.main()
