from api.chat_api import submit_chat_request
from ui.cli import get_user_input, show_error, show_output

DATA_FILE = "data/messages.json"


def main() -> None:
    """
    程序主入口：
    1. 从 UI 层读取用户输入
    2. 交给 API 层处理请求
    3. 显示返回结果或错误信息
    """
    try:
        user_input = get_user_input()
        payload = {"message": user_input}
        response = submit_chat_request(payload, DATA_FILE)
        show_output(response["reply"])
    except Exception as exc:
        show_error(str(exc))


if __name__ == "__main__":
    main()
