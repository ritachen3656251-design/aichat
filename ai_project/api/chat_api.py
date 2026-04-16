from services.chat_service import handle_chat
from utils.logger import log_error, log_input, log_output
from utils.validators import validate_chat_payload


def submit_chat_request(payload: dict, filepath: str) -> dict:
    """
    模拟一个轻量 API 层。

    职责：
    - 接收请求参数
    - 校验请求参数
    - 调用服务层
    - 返回标准响应字典
    """
    try:
        log_input(f"API received payload={payload}")
        validate_chat_payload(payload)

        user_message = payload["message"]
        reply = handle_chat(user_message, filepath)

        response = {"success": True, "reply": reply}
        log_output(f"API response={response}")
        return response
    except Exception as exc:
        log_error(f"API failed: {exc}")
        raise
