import json

from typing import Union, Dict
from functools import wraps

from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response


def RequiredMethod(method: Union[str, list]):
    """
    请求方式限制装饰器

    :param method: 允许的请求方法
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if isinstance(method, str):
                if request.method == method:
                    return func(request)
                else:
                    return process_response(request, ResponseStatus.REQUEST_METHOD_ERROR)
            elif isinstance(method, list):
                if request.method in method:
                    return func(request)
                else:
                    return process_response(request, ResponseStatus.REQUEST_METHOD_ERROR)
            else:
                return process_response(request, ResponseStatus.UNEXPECTED_ERROR)

        return wrapper

    return decorator


def RequiredParameters(parameters: Dict[str, ResponseStatus]):
    """
    参数存在性判断装饰器

    :param parameters: 要求的参数与对应的错误
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            # JSON 解析
            if not hasattr(request, 'json_data') or not isinstance(request.json_data, dict):
                try:
                    request.json_data = json.loads(request.body)
                except json.JSONDecodeError:
                    request.json_data = None
                if request.json_data is None:
                    return process_response(request, ResponseStatus.JSON_DECODE_ERROR)

            # 参数存在性判断
            for param in parameters:
                if param not in request.json_data or not request.json_data[param]:
                    return process_response(request, parameters[param])

            # 正常处理
            return func(request)

        return wrapper

    return decorator
