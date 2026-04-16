from data.storage import load_messages, save_messages
from models.llm_client import generate_reply
from utils.logger import log_error, log_input, log_output
from utils.validators import validate_user_input


def handle_chat(user_input: str, filepath: str) -> str:
    """
    核心业务流程：
    - 校验用户输入
    - 读取已有消息
    - 追加用户消息
    - 生成回复内容
    - 追加助手消息
    - 保存完整会话
    - 返回回复结果
    """
    try:
        log_input(f"Service received user_input={user_input!r}")
        validate_user_input(user_input)

        messages = load_messages(filepath)
        log_output(f"Loaded {len(messages)} existing messages")

        messages.append({"role": "user", "content": user_input})

        reply = generate_reply(messages)
        log_output(f"Model reply={reply!r}")

        messages.append({"role": "assistant", "content": reply})

        save_messages(filepath, messages)
        log_output("Messages saved successfully")

        return reply
    except Exception as exc:
        log_error(f"Service failed: {exc}")
        raise
