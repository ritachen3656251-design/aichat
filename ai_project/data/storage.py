import json
import os

from utils.exceptions import DataValidationError
from utils.logger import log_error, log_output


def load_messages(filepath: str) -> list:
    """
    从 JSON 文件中读取消息列表。

    支持的边界情况：
    - 文件不存在：返回空列表
    - 文件为空：返回空列表
    - JSON 非法：抛出 DataValidationError
    - JSON 顶层不是列表：抛出 DataValidationError
    """
    if not os.path.exists(filepath):
        log_output(f"Data file not found, initialize empty list: {filepath}")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            raw = file.read().strip()

        if not raw:
            log_output(f"Data file is empty, treat as empty list: {filepath}")
            return []

        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        log_error(f"Invalid JSON in {filepath}: {exc}")
        raise DataValidationError("messages.json is not valid JSON") from exc

    if not isinstance(data, list):
        raise DataValidationError("messages.json top-level structure must be a list")

    return data


def save_messages(filepath: str, messages: list) -> None:
    """
    将消息列表保存到 JSON 文件中。
    """
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=2)

    log_output(f"Saved {len(messages)} messages to {filepath}")
