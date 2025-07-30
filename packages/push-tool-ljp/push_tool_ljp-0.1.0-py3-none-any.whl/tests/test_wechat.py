import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from push_tool.wechat import WeChatBot

class TestWeChatBot(unittest.TestCase):
    def setUp(self):
        self.webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test"
        self.bot = WeChatBot(self.webhook_url)

    @patch('push_tool.wechat.requests.Session.post')
    def test_send_text(self, mock_post):
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}
        mock_post.return_value = mock_response

        # 测试发送文本消息
        result = self.bot.send_text("Hello, World!", ["user1"])

        # 验证请求构造
        expected_payload = {
            "msgtype": "text",
            "text": {
                "content": "Hello, World!",
                "mentioned_list": ["user1"]
            }
        }
        mock_post.assert_called_once_with(
            self.webhook_url,
            json=expected_payload,
            timeout=10
        )

        # 验证返回结果
        self.assertEqual(result, {"errcode": 0, "errmsg": "ok"})

    @patch('push_tool.wechat.requests.Session.post')
    def test_send_image(self, mock_post):
        # 模拟上传和发送响应
        upload_response = MagicMock()
        upload_response.json.return_value = {"media_id": "test_media_id"}

        send_response = MagicMock()
        send_response.json.return_value = {"errcode": 0, "errmsg": "ok"}

        mock_post.side_effect = [upload_response, send_response]

        # 测试发送图片消息
        with patch('builtins.open', unittest.mock.mock_open(read_data=b'test')):
            result = self.bot.send_image(r"C:\Users\LJP\Desktop\spider\包开发\1.png")

        # 验证请求构造
        self.assertEqual(mock_post.call_count, 2)

        # 验证返回结果
        self.assertEqual(result, {"errcode": 0, "errmsg": "ok"})

    def test_upload_media_file_not_found(self):
        # 测试文件不存在时的错误处理
        with self.assertRaises(FileNotFoundError):
            self.bot._upload_media("nonexistent.jpg", "image")

if __name__ == '__main__':
    unittest.main()
