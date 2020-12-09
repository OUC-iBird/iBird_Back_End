import re
import os
import json

import requests
from ratelimit.decorators import ratelimit
from django.core.paginator import Paginator

from iBird import settings
from apps.utils.decorator import RequiredMethod, RequiredParameters, Protect, LoginRequired
from apps.utils.response_status import ResponseStatus, ValueErrorStatus
from apps.utils.response_processor import process_response
from apps.account import models as account_models
from apps.prediction import models as prediction_models
from apps.gallery import models as gallery_models


@Protect
@RequiredMethod('POST')
@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@LoginRequired
@RequiredParameters('path', 'longitude', 'latitude')
def save_in_gallery(request):
    json_data = request.json_data

    status = ValueErrorStatus.check_value_type(json_data)
    if status is not None:
        return process_response(request, status)

    path = json_data['path']
    if len(path) > 100 or re.search(r'\.\.', path) or path[:9] != '/' + settings.PICTURE_PATH \
            or not os.path.exists('.' + path):
        return process_response(request, ResponseStatus.IMAGE_PATH_NOT_FOUND_ERROR)

    longitude = json_data['longitude']
    latitude = json_data['latitude']
    address = ''
    if longitude != 0.0 and latitude != 0.0:
        try:
            result = requests.get(settings.BAIDU_ADDRESS_API_URL.format(longitude=longitude, latitude=latitude))
            if result.status_code == 200:
                address = json.loads(result.text)['result']['formatted_address']
        except Exception:
            address = ''

    user = account_models.User.objects.filter(username=request.session.get('username')).first()
    report = prediction_models.Report.objects.filter(path=path).first()

    photo = gallery_models.Photo(user=user, path=path, report=report, address=address,
                                 latitude=latitude, longitude=longitude)
    photo.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
@ratelimit(**settings.RATE_LIMIT_LEVEL_3)
@LoginRequired
def get_my_gallery(request):
    num = request.GET.get('num')
    if not num:
        num = 1
    else:
        status = ValueErrorStatus.check_value_type({'num': num})
        if status is not None:
            return process_response(request, status)
        num = int(num)

    user = account_models.User.objects.filter(username=request.session.get('username')).first()
    photos = gallery_models.Photo.objects.filter(user=user).order_by('-id')

    paginator = Paginator(photos, settings.PHOTOS_PER_PAGE)
    total = paginator.num_pages

    if not 1 <= num <= total:
        return process_response(request, ResponseStatus.NUM_OUT_OF_RANGE_ERROR)

    page = paginator.page(num)

    photos_path = []
    for one in page.object_list:
        photos_path.append(one.path)

    request.data = {
        'photo': photos_path,
        'count': len(photos_path),
        'num': num,
        'has_next': page.has_next()
    }

    return process_response(request, ResponseStatus.OK)
