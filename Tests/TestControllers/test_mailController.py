from unittest import TestCase, mock

from Controllers import mailController
mc = mailController.MailControl()


class TestMailController(TestCase):

    @mock.patch("Controllers.mailController.smtplib")
    @mock.patch("Controllers.mailController.MIMEMultipart")
    def test_send_mail_works(self, mock_MIMEMultipart, mock_smtplib):
        receiver = "email@email.com"
        title = "test"
        message = "message..."
        mock_MIMEMultipart.return_value = None
        self.assertFalse(mc.send_mail(receiver, title, message))

        mock_MIMEMultipart.return_value = mock.MagicMock()
        mock_MIMEMultipart.__getitem__.return_value = ""
        self.assertTrue(mc.send_mail(receiver, title, message))
