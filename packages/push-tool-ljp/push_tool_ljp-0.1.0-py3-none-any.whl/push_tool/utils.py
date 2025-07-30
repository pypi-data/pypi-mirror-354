import os
import logging
from typing import Optional, Dict, Any, Union
from pathlib import Path
from dotenv import load_dotenv

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    # 默认从.env文件加载
    if config_path is None:
        config_path = ".env"

    if not Path(config_path).exists():
        return {}

    load_dotenv(config_path)
    return dict(os.environ)

def setup_logging(
    log_file: Optional[str] = None,
    log_level: int = logging.INFO
) -> None:
    """
    配置日志记录

    Args:
        log_file: 日志文件路径(不指定则只输出到控制台)
        log_level: 日志级别
    """
    handlers = [logging.StreamHandler()]

    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def validate_file_path(file_path: Union[str, Path]) -> Path:
    """
    验证文件路径是否存在

    Args:
        file_path: 文件路径

    Returns:
        验证后的Path对象

    Raises:
        FileNotFoundError: 如果文件不存在
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path
