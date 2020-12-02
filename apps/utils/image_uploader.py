import time
import re
import os

import magic
from ratelimit.decorators import ratelimit

from iBird import settings
from apps.utils.decorator import RequiredMethod, Protect
from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus
from apps.utils.random_string_generator import generate_string, Pattern


@Protect
@ratelimit(**settings.RATE_LIMIT_LEVEL_1)
@RequiredMethod('POST')
def upload(request):
    # 图片
    img = request.FILES.get('img')
    if not img:
        return process_response(request, ResponseStatus.IMAGE_REQUIRED_ERROR)

    # 用途
    usage = request.POST.get('usage')
    if not usage:
        return process_response(request, ResponseStatus.USAGE_REQUIRED_ERROR)
    if usage not in settings.IMAGE_USAGE:
        return process_response(request, ResponseStatus.USAGE_NOT_CORRECT_ERROR)

    # 图片大小
    if img.size > settings.IMAGE_MAX_SIZE:
        return process_response(request, ResponseStatus.IMAGE_SIZE_TOO_LARGE_ERROR)

    # 图片后缀名初步判断图片类型
    extension = img.name.split('.')[-1]
    if extension not in settings.ALLOWED_IMAGE_EXTENSION:
        return process_response(request, ResponseStatus.IMAGE_EXTENSION_NOT_ALLOWED_ERROR)

    # 图片名 当前时间 + 随机字符串
    img_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + generate_string(10, Pattern.Lowercase_And_Digits)

    # 图片保存路径
    path = settings.IMAGE_USAGE[usage] + img_name + '.' + extension

    # 储存图片
    with open(path, 'wb') as f:
        for chunk in img.chunks():
            f.write(chunk)

    # 精确判断图片类型
    if not re.search(settings.ALLOWED_IMAGE_EXTENSION[extension], magic.from_file(path)):
        if os.path.exists(path):
            os.remove(path)
        return process_response(request, ResponseStatus.IMAGE_EXTENSION_NOT_ALLOWED_ERROR)

    request.data = {
        'path': '/' + path
    }

    return process_response(request, ResponseStatus.OK)
