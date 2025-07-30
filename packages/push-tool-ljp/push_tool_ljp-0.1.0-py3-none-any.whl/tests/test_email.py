import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from push_tool.email import EmailSender

class TestEmailSender(unittest.TestCase):
    def setUp(self):
        self.smtp_server = "smtp.example.com"
        self.smtp_port = 587
        self.username = "user@example.com"
        self.password = "password"
        self.sender = EmailSender(
            self.smtp_server,
            self.smtp_port,
            self.username,
            self.password
        )

    @patch('smtplib.SMTP')
    def test_send_plain_text_email(self, mock_smtp):
        # 设置模拟SMTP
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # 测试发送纯文本邮件
        result = self.sender.send_email(
            subject="Test Subject",
            content="Test Content",
            to_addrs="recipient@example.com"
        )

        # 验证SMTP调用
        mock_smtp.assert_called_once_with(self.smtp_server, self.smtp_port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with(self.username, self.password)
        mock_server.send_message.assert_called_once()

        # 验证返回结果
        self.assertTrue(result)

    @patch('smtplib.SMTP')
    def test_send_html_email(self, mock_smtp):
        # 设置模拟SMTP
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # 测试发送HTML邮件
        result = self.sender.send_email(
            subject="HTML Test",
            content="<h1>HTML Content</h1>",
            to_addrs="recipient@example.com",
            html=True
        )

        # 验证SMTP调用
        mock_server.send_message.assert_called_once()

        # 验证返回结果
        self.assertTrue(result)

    @patch('smtplib.SMTP')
    def test_send_email_with_attachment(self, mock_smtp):
        # 设置模拟SMTP
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # 测试发送带附件邮件
        with patch('builtins.open', unittest.mock.mock_open(read_data=b'test')):
            result = self.sender.send_email(
                subject="With Attachment",
                content="See attachment",
                to_addrs="recipient@example.com",
                attachments=["test.txt"]
            )

        # 验证SMTP调用
        mock_server.send_message.assert_called_once()

        # 验证返回结果
        self.assertTrue(result)

    @patch('smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp):
        # 模拟SMTP错误
        mock_smtp.side_effect = Exception("SMTP Error")

        # 测试发送失败情况
        with self.assertRaises(RuntimeError):
            self.sender.send_email(
                subject="Test",
                content="Content",
                to_addrs="recipient@example.com"
            )

if __name__ == '__main__':
    unittest.main()
