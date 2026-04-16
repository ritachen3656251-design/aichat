from utils.exceptions import RequestValidationError


def validate_chat_payload(payload: dict) -> None:
    """
    校验 API 请求参数。
    """
    if not isinstance(payload, dict):
        raise RequestValidationError("payload must be a dict")

    if "message" not in payload:
        raise RequestValidationError("payload is missing required field: message")

    if not isinstance(payload["message"], str):
        raise RequestValidationError("message must be a string")


def validate_user_input(user_input: str) -> None:
    """
    校验用户输入内容。
    """
    if not isinstance(user_input, str):
        raise RequestValidationError("user_input must be a string")

    if not user_input.strip():
        raise RequestValidationError("user_input cannot be empty")

    if len(user_input) > 200:
        raise RequestValidationError("user_input cannot exceed 200 characters")
