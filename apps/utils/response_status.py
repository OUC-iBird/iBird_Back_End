from enum import Enum


class ResponseStatus(Enum):
    """
    响应状态的枚举类

    状态类型格式形如:
    Status_Name = (code: int, message: str)
    """
    # 成功
    OK = (20000, '成功')

    # 意外错误
    UNEXPECTED_ERROR = (50000, '意外错误')
