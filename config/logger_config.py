# config/logger_config.py
import os
import sys
from pathlib import Path  # 使用 pathlib 处理路径更方便
from loguru import logger


def setup_logger():
    """配置全局日志."""

    # 移除默认的处理器
    logger.remove()

    log_dir = Path("logs")  # 将 log_dir 定义为 Path 对象

    # 检查日志目录是否存在，如果不存在则创建
    log_dir.mkdir(parents=True, exist_ok=True)  # 使用 pathlib 的 mkdir

    # 设置日志文件路径
    info_log_file = log_dir / "info.log"       # 使用 / 运算符连接路径
    error_log_file = log_dir / "error.log"
    warning_log_file = log_dir / "warning.log"

    # 添加 INFO 日志处理器
    logger.add(
        str(info_log_file),  # 传递 str(log_file)
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8",
        enqueue=True,
        filter=lambda record: record["level"].name == "INFO"
    )

    # 添加 WARNING 日志处理器
    logger.add(
        str(warning_log_file),  # 传递 str(log_file)
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        level="WARNING",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8",
        enqueue=True,
        filter=lambda record: record["level"].name == "WARNING"
    )

    # 添加 ERROR 日志处理器
    logger.add(
        str(error_log_file),  # 传递 str(log_file)
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        encoding="utf-8",
        enqueue=True,
        filter=lambda record: record["level"].name == "ERROR"
    )

    # 添加控制台输出处理器（输出所有级别的日志）
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="INFO",
    )


# 调用 setup_logger() 方法以配置全局日志
setup_logger()

# 导出 logger，可以供其他模块直接调用
__all__ = ["logger"]        # 只需公开 logger，setup_logger 不需要公开