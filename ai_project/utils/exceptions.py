class RequestValidationError(Exception):
    """
    请求参数或用户输入不合法。
    """


class DataValidationError(Exception):
    """
    持久化数据结构错误，或 JSON 内容损坏。
    """


class ModelError(Exception):
    """
    模型层相关错误。
    """
