def get_user_input() -> str:
    """
    从命令行读取用户输入。
    """
    return input("You: ").strip()


def show_output(text: str) -> None:
    """
    显示正常输出。
    """
    print(f"AI: {text}")


def show_error(message: str) -> None:
    """
    显示错误信息。
    """
    print(f"[UI ERROR] {message}")
