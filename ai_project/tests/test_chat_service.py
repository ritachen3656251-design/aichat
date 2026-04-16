import json
import os
import shutil
import unittest
import uuid

from api.chat_api import submit_chat_request
from data.storage import load_messages
from services.chat_service import handle_chat
from utils.exceptions import DataValidationError, ModelError, RequestValidationError


class TestChatProject(unittest.TestCase):
    def setUp(self) -> None:
        """
        为每个测试创建独立的临时 JSON 文件目录。
        """
        self.temp_dir = os.path.join(os.getcwd(), "test_runtime", uuid.uuid4().hex)
        os.makedirs(self.temp_dir, exist_ok=True)
        self.filepath = os.path.join(self.temp_dir, "messages.json")

    def tearDown(self) -> None:
        """
        每个测试结束后清理临时目录。
        """
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        runtime_root = os.path.join(os.getcwd(), "test_runtime")
        if os.path.isdir(runtime_root) and not os.listdir(runtime_root):
            os.rmdir(runtime_root)

    def test_handle_chat_success(self) -> None:
        """
        正常路径：保存用户消息和助手消息。
        """
        reply = handle_chat("hello", self.filepath)

        self.assertEqual(reply, "I received your input: hello")

        messages = load_messages(self.filepath)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "hello")
        self.assertEqual(messages[1]["role"], "assistant")
        self.assertEqual(messages[1]["content"], "I received your input: hello")

    def test_handle_chat_empty_input(self) -> None:
        with self.assertRaises(RequestValidationError):
            handle_chat("", self.filepath)

    def test_handle_chat_whitespace_input(self) -> None:
        with self.assertRaises(RequestValidationError):
            handle_chat("   ", self.filepath)

    def test_handle_chat_too_long_input(self) -> None:
        with self.assertRaises(RequestValidationError):
            handle_chat("a" * 201, self.filepath)

    def test_submit_chat_request_missing_message(self) -> None:
        with self.assertRaises(RequestValidationError):
            submit_chat_request({}, self.filepath)

    def test_submit_chat_request_wrong_message_type(self) -> None:
        with self.assertRaises(RequestValidationError):
            submit_chat_request({"message": 123}, self.filepath)

    def test_invalid_json_file(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as file:
            file.write("{ bad json")

        with self.assertRaises(DataValidationError):
            handle_chat("hello", self.filepath)

    def test_wrong_top_level_json_structure(self) -> None:
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump({"role": "user"}, file, ensure_ascii=False)

        with self.assertRaises(DataValidationError):
            handle_chat("hello", self.filepath)

    def test_model_error(self) -> None:
        with self.assertRaises(ModelError):
            handle_chat("trigger model error", self.filepath)


if __name__ == "__main__":
    unittest.main()
