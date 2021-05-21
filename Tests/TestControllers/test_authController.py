from unittest import TestCase, mock
from config import KEY
from Controllers import authController
import base64
ac = authController.AuthControl()


class TestAuthController(TestCase):
    def test_password_encode_works(self):
        self.assertEqual(ac.password_encode("testepassword"), "dGVzdGVwYXNzd29yZA==")
        self.assertEqual(ac.password_encode([]), "")
        self.assertEqual(ac.password_encode({}), "")

    def test_password_is_encoded_works(self):
        self.assertFalse(ac.password_is_encoded("testpassword"))
        self.assertTrue(ac.password_is_encoded("dGVzdGVwYXNzd29yZA=="))

    def test_password_decode_works(self):
        self.assertEqual(ac.password_decode("dGVzdGVwYXNzd29yZA=="), "testepassword")
        self.assertEqual(ac.password_decode("test"), "")

    def test_access_key_validation_works(self):
        self.assertTrue(ac.access_key_validation(dict(Key=KEY)))
        self.assertFalse(ac.access_key_validation(dict(Key="AccessKey")))
        self.assertFalse(ac.access_key_validation(dict()))

    @mock.patch("Controllers.authController.Fernet")
    def test_encrypt_works(self, mock_Fernet):
        mock_Fernet.return_value = mock.MagicMock()
        mock_Fernet().encrypt.return_value = bytes("kjzgBRBJMOP6d4fQhzqcr4Poheiona".encode())
        content = "testing..."
        key = "YTZTMkXyaOJ9Eum7yJewx7Ayy6MZSk8LdmDagZOxyWg="
        encrypt = ac.encrypt(content, key)
        self.assertEqual(type(encrypt), bytes)
        self.assertEqual(encrypt, bytes("kjzgBRBJMOP6d4fQhzqcr4Poheiona".encode()))

    def test_is_encrypted(self):
        self.assertTrue(ac.is_encrypted(bytes("test".encode())))
        self.assertFalse(ac.is_encrypted("test"))

    @mock.patch("Controllers.authController.Fernet")
    def test_decrypt(self, mock_Fernet):
        content_encrypted = bytes("kjzgBRBJMOP6d4fQhzqcr4Poheiona".encode())
        mock_Fernet.return_value = mock.MagicMock()
        mock_Fernet().decrypt.return_value = content_encrypted
        key = "YTZTMkXyaOJ9Eum7yJewx7Ayy6MZSk8LdmDagZOxyWg="
        self.assertEqual(ac.decrypt(content_encrypted, key), "kjzgBRBJMOP6d4fQhzqcr4Poheiona")

