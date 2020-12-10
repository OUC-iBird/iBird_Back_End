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

    CAPTCHA_REQUIRED_ERROR = (41001, '缺少验证码')
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
    LONGITUDE_REQUIRED_ERROR = (41012, '缺少经度')
    LATITUDE_REQUIRED_ERROR = (41013, '缺少纬度')
    NUM_REQUIRED_ERROR = (41014, '缺少页号')
    CONTENT_REQUIRED_ERROR = (41015, '缺少内容')
    POST_ID_REQUIRED_ERROR = (41016, '缺少动态 ID')
    NICKNAME_REQUIRED_ERROR = (41017, '缺少昵称')
    AVATAR_REQUIRED_ERROR = (41018, '缺少头像')

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
    NUM_OUT_OF_RANGE_ERROR = (42013, '页号超出范围')
    CONTENT_LENGTH_TOO_LARGE_ERROR = (42014, '内容过长')
    NICKNAME_LENGTH_TOO_LARGE_ERROR = (42015, '昵称过长')

    USERNAME_EXISTED_ERROR = (43001, '用户名已存在')
    EMAIL_EXISTED_ERROR = (43002, '邮箱已存在')
    USERNAME_NOT_EXISTED_ERROR = (43003, '用户名不存在')
    PASSWORD_NOT_MATCH_ERROR = (43004, '密码错误')
    VERIFY_CODE_NOT_MATCH_ERROR = (43005, '验证码不匹配')
    IMAGE_PATH_NOT_FOUND_ERROR = (43006, '图片路径不存在')
    REPORT_NOT_EXISTED_ERROR = (43007, '报告不存在')
    BIRD_ID_NOT_EXISTED_ERROR = (43008, '鸟类编号不存在')
    PHOTO_EXISTED_ERROR = (43009, '图片已存在')
    POST_NOT_FOUND_ERROR = (43010, '动态不存在')
    LIKE_ALREADY_ERROR = (43011, '已点赞')

    NOT_LOGIN = (44001, '未登陆')

    CAPTCHA_VALUE_ERROR = (45001, '验证码类型错误')
    USERNAME_VALUE_ERROR = (45002, '用户名类型错误')
    PASSWORD_VALUE_ERROR = (45003, '密码类型错误')
    EMAIL_VALUE_ERROR = (45004, '邮箱类型错误')
    NEW_PASSWORD_VALUE_ERROR = (45005, '新密码类型错误')
    VERIFY_CODE_VALUE_ERROR = (45006, '验证码类型错误')
    IMAGE_VALUE_ERROR = (45007, '图片类型错误')
    USAGE_VALUE_ERROR = (45008, '用途类型错误')
    IMAGE_PATH_VALUE_ERROR = (45009, '图片路径类型错误')
    SEQUENCE_VALUE_ERROR = (45010, '序列号类型错误')
    BIRD_ID_VALUE_ERROR = (45011, '鸟类编号类型错误')
    LONGITUDE_VALUE_ERROR = (45012, '经度类型错误')
    LATITUDE_VALUE_ERROR = (45013, '纬度类型错误')
    NUM_VALUE_ERROR = (45014, '页号类型错误')
    CONTENT_VALUE_ERROR = (45015, '内容类型错误')
    POST_ID_VALUE_ERROR = (45016, '动态 ID 类型错误')
    NICKNAME_VALUE_ERROR = (45017, '昵称类型错误')
    AVATAR_VALUE_ERROR = (45018, '头像类型错误')


class RequiredErrorStatus:
    """
    要求参数缺失状态的映射类
    """
    __required_error_map = {
        'captcha': ResponseStatus.CAPTCHA_REQUIRED_ERROR,
        'username': ResponseStatus.USERNAME_REQUIRED_ERROR,
        'password': ResponseStatus.PASSWORD_REQUIRED_ERROR,
        'email': ResponseStatus.EMAIL_REQUIRED_ERROR,
        'new_password': ResponseStatus.NEW_PASSWORD_REQUIRED_ERROR,
        'verify_code': ResponseStatus.VERIFY_CODE_REQUIRED_ERROR,
        'img': ResponseStatus.IMAGE_REQUIRED_ERROR,
        'usage': ResponseStatus.USAGE_REQUIRED_ERROR,
        'path': ResponseStatus.IMAGE_PATH_REQUIRED_ERROR,
        'sequence': ResponseStatus.SEQUENCE_REQUIRED_ERROR,
        'bird_id': ResponseStatus.BIRD_ID_REQUIRED_ERROR,
        'longitude': ResponseStatus.LONGITUDE_REQUIRED_ERROR,
        'latitude': ResponseStatus.LATITUDE_REQUIRED_ERROR,
        'num': ResponseStatus.NUM_REQUIRED_ERROR,
        'content': ResponseStatus.CONTENT_REQUIRED_ERROR,
        'post_id': ResponseStatus.POST_ID_REQUIRED_ERROR,
        'nickname': ResponseStatus.NICKNAME_REQUIRED_ERROR,
        'avatar': ResponseStatus.AVATAR_REQUIRED_ERROR
    }

    @classmethod
    def get_required_error_status(cls, param):
        if param in cls.__required_error_map:
            return cls.__required_error_map[param]
        else:
            return ResponseStatus.UNEXPECTED_ERROR


class ValueType(Enum):
    STRING = 1
    INTEGER = 2
    FLOAT = 3


class ValueErrorStatus:
    __value_error_map = {
        'captcha': ResponseStatus.CAPTCHA_VALUE_ERROR,
        'username': ResponseStatus.USERNAME_VALUE_ERROR,
        'password': ResponseStatus.PASSWORD_VALUE_ERROR,
        'email': ResponseStatus.EMAIL_VALUE_ERROR,
        'new_password': ResponseStatus.NEW_PASSWORD_VALUE_ERROR,
        'verify_code': ResponseStatus.VERIFY_CODE_VALUE_ERROR,
        'img': ResponseStatus.IMAGE_VALUE_ERROR,
        'usage': ResponseStatus.USAGE_VALUE_ERROR,
        'path': ResponseStatus.IMAGE_PATH_VALUE_ERROR,
        'sequence': ResponseStatus.SEQUENCE_VALUE_ERROR,
        'bird_id': ResponseStatus.BIRD_ID_VALUE_ERROR,
        'longitude': ResponseStatus.LONGITUDE_VALUE_ERROR,
        'latitude': ResponseStatus.LATITUDE_VALUE_ERROR,
        'num': ResponseStatus.NUM_VALUE_ERROR,
        'content': ResponseStatus.CONTENT_VALUE_ERROR,
        'post_id': ResponseStatus.POST_ID_VALUE_ERROR,
        'nickname': ResponseStatus.NICKNAME_VALUE_ERROR,
        'avatar': ResponseStatus.AVATAR_VALUE_ERROR
    }

    __value_type_map = {
        'captcha': ValueType.STRING,
        'username': ValueType.STRING,
        'password': ValueType.STRING,
        'email': ValueType.STRING,
        'new_password': ValueType.STRING,
        'verify_code': ValueType.STRING,
        'img': ValueType.STRING,
        'usage': ValueType.STRING,
        'path': ValueType.STRING,
        'sequence': ValueType.INTEGER,
        'bird_id': ValueType.INTEGER,
        'longitude': ValueType.FLOAT,
        'latitude': ValueType.FLOAT,
        'num': ValueType.INTEGER,
        'content': ValueType.STRING,
        'post': ValueType.INTEGER,
        'nickname': ValueType.STRING,
        'avatar': ValueType.STRING
    }

    @classmethod
    def check_value_type(cls, data: dict):
        for key in data:
            if key not in cls.__value_type_map:
                continue

            value_type = cls.__value_type_map[key]
            if value_type == ValueType.STRING:
                if not isinstance(data[key], str):
                    try:
                        data[key] = str(data[key])
                    except ValueError:
                        return cls.__value_error_map[key]
            elif value_type == ValueType.INTEGER:
                if not isinstance(data[key], int):
                    try:
                        data[key] = int(data[key])
                    except ValueError:
                        return cls.__value_error_map[key]
            elif value_type == ValueType.FLOAT:
                if not isinstance(data[key], float):
                    try:
                        data[key] = float(data[key])
                    except ValueError:
                        return cls.__value_error_map[key]
        return None
