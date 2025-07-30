import unittest
import os
import logging
from unittest.mock import patch
from push_tool.utils import load_config, setup_logging, validate_file_path

class TestUtils(unittest.TestCase):
    @patch('push_tool.utils.load_dotenv')
    def test_load_config(self, mock_load_dotenv):
        # 测试加载配置文件
        result = load_config("test.env")

        # 验证dotenv被调用
        mock_load_dotenv.assert_called_once_with("test.env")

    def test_setup_logging(self):
        # 测试日志配置
        with patch('logging.basicConfig') as mock_basic_config:
            setup_logging(log_level=logging.DEBUG)

            # 验证日志配置
            mock_basic_config.assert_called_once()
            args, kwargs = mock_basic_config.call_args
            self.assertEqual(kwargs['level'], logging.DEBUG)

    def test_validate_file_path(self):
        # 测试文件路径验证
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True

            # 验证存在的文件路径
            path = validate_file_path("existing.txt")
            self.assertEqual(str(path), "existing.txt")

            # 测试不存在的文件路径
            mock_exists.return_value = False
            with self.assertRaises(FileNotFoundError):
                validate_file_path("nonexistent.txt")

if __name__ == '__main__':
    unittest.main()
