from utils.exceptions import ModelError


def generate_reply(messages: list) -> str:
    """
    使用最后一条用户消息模拟模型回复。
    """
    if not isinstance(messages, list):
        raise ModelError("messages must be a list")

    if not messages:
        raise ModelError("messages cannot be empty")

    last_message = messages[-1]

    if not isinstance(last_message, dict):
        raise ModelError("the last message must be a dict")

    if last_message.get("role") != "user":
        raise ModelError("the last message must come from the user")

    content = last_message.get("content")

    if not isinstance(content, str):
        raise ModelError("message content must be a string")

    if content == "trigger model error":
        raise ModelError("simulated model failure triggered")

    return f"I received your input: {content}"
