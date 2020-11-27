"""
仅供测试 仅供测试 仅供测试 仅供测试 仅供测试 仅供测试 仅供测试
"""
from django_redis import get_redis_connection

from apps.utils.decorator import RequiredMethod, RequiredParameters
from apps.utils.response_processor import process_response
from apps.utils.response_status import ResponseStatus


@RequiredMethod('GET')
def test_get(request):
    cache = get_redis_connection('default')
    test_value = cache.get('test')
    if not test_value or len(test_value) > 200:
        test_value = 'Hello World'
        cache.set('test', test_value)

    request.data = {
        'test_value': test_value
    }

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('POST')
@RequiredParameters('username')
def test_post(request):
    cache = get_redis_connection('default')
    json_data = request.json_data

    test_value = cache.get('test')
    if not test_value or len(test_value) > 200:
        test_value = 'Hello World'
        cache.set('test', test_value)

    cache.set('test', json_data['username'])

    request.data = {}
    for one in json_data:
        if one != 'username':
            request.data[one] = json_data[one]

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('PATCH')
@RequiredParameters('username')
def test_patch(request):
    cache = get_redis_connection('default')
    json_data = request.json_data

    test_value = cache.get('test')
    if not test_value or len(test_value) > 200:
        test_value = 'Hello World'
        cache.set('test', test_value)

    cache.set('test', test_value + json_data['username'])

    request.data = {}
    for one in json_data:
        if one != 'username':
            request.data[one] = json_data[one]

    return process_response(request, ResponseStatus.OK)
