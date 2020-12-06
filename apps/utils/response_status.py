from enum import Enum


class ResponseStatus(Enum):
    """
    响应状态的枚举类

    状态类型格式形如:
    Status_Name = (code: int, message: str)
    """
    # Debug
    DEBUG = (10000, 'Debug')

    # 成功
    OK = (20000, '成功')

    # 禁止访问
    FORBIDDEN = (50403, 'Forbidden')

    # 意外错误
    UNEXPECTED_ERROR = (50000, '意外错误')

    # 正常错误
    REQUEST_METHOD_ERROR = (40000, '请求方法错误')
    JSON_DECODE_ERROR = (40001, 'JSON 解析错误')

    CAPTCHA_ERROR_ERROR = (41001, '缺少验证码')
    USERNAME_REQUIRED_ERROR = (41002, '缺少用户名')
    PASSWORD_REQUIRED_ERROR = (41003, '缺少密码')
    EMAIL_REQUIRED_ERROR = (41004, '缺少邮箱')
    NEW_PASSWORD_REQUIRED_ERROR = (41005, '缺少新密码')
    VERIFY_CODE_REQUIRED_ERROR = (41006, '缺少验证码')
    IMAGE_REQUIRED_ERROR = (41007, '缺少图片')
    USAGE_REQUIRED_ERROR = (41008, '缺少用途')
    IMAGE_PATH_REQUIRED_ERROR = (41009, '缺少图片路径')
    SEQUENCE_REQUIRED_ERROR = (41010, '缺少序列号')
    BIRD_ID_REQUIRED_ERROR = (41011, '缺少鸟类编号')

    USERNAME_TOO_SHORT_ERROR = (42001, '用户名应不少于 4 位')
    USERNAME_TOO_LONG_ERROR = (42002, '用户名应不多于 20 位')
    USERNAME_FORMAT_ERROR = (42003, '用户名仅能含有字母、数字和下划线')
    PASSWORD_TOO_SHORT_ERROR = (42004, '密码应不少于 6 位')
    PASSWORD_TOO_LONG_ERROR = (42005, '密码应不多于 20 位')
    PASSWORD_FORMAT_ERROR = (42006, '密码应仅包含合法字符')
    PASSWORD_LACK_NUMBER_ERROR = (42007, '密码必须包含数字')
    PASSWORD_LACK_LETTER_ERROR = (42008, '密码必须包含字母')
    EMAIL_FORMAT_ERROR = (42009, '邮箱格式错误')
    USAGE_NOT_CORRECT_ERROR = (42010, '图片用途错误')
    IMAGE_SIZE_TOO_LARGE_ERROR = (42011, '图片大小不得超过 5MB')
    IMAGE_EXTENSION_NOT_ALLOWED_ERROR = (42012, '图片仅支持 jpg, png 格式')

    USERNAME_EXISTED_ERROR = (43001, '用户名已存在')
    EMAIL_EXISTED_ERROR = (43002, '邮箱已存在')
    USERNAME_NOT_EXISTED_ERROR = (43003, '用户名不存在')
    PASSWORD_NOT_MATCH_ERROR = (43004, '密码错误')
    VERIFY_CODE_NOT_MATCH_ERROR = (43005, '验证码不匹配')
    IMAGE_PATH_NOT_FOUND_ERROR = (43006, '图片路径不存在')
    REPORT_NOT_EXISTED_ERROR = (43007, '报告不存在')
    BIRD_ID_NOT_EXISTED_ERROR = (43008, '鸟类编号不存在')

    NOT_LOGIN = (44001, '未登陆')


class RequiredErrorStatus:
    """
    要求参数缺失状态的映射类
    """
    __required_error_map = {
        'captcha': ResponseStatus.CAPTCHA_ERROR_ERROR,
        'username': ResponseStatus.USERNAME_REQUIRED_ERROR,
        'password': ResponseStatus.PASSWORD_REQUIRED_ERROR,
        'email': ResponseStatus.EMAIL_REQUIRED_ERROR,
        'new_password': ResponseStatus.NEW_PASSWORD_REQUIRED_ERROR,
        'verify_code': ResponseStatus.VERIFY_CODE_REQUIRED_ERROR,
        'img': ResponseStatus.IMAGE_REQUIRED_ERROR,
        'usage': ResponseStatus.USAGE_REQUIRED_ERROR,
        'path': ResponseStatus.IMAGE_PATH_REQUIRED_ERROR,
        'sequence': ResponseStatus.SEQUENCE_REQUIRED_ERROR,
        'bird_id': ResponseStatus.BIRD_ID_REQUIRED_ERROR
    }

    @classmethod
    def get_required_error_status(cls, param):
        if param in cls.__required_error_map:
            return cls.__required_error_map[param]
        else:
            return ResponseStatus.UNEXPECTED_ERROR
