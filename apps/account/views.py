from django.contrib.auth.hashers import make_password, check_password

from apps.utils.decorator import RequiredMethod, RequiredParameters
from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response
from apps.utils.validator import validate_username, validate_password, validate_email
from apps.account import models as account_models


@RequiredMethod('POST')
@RequiredParameters({'username': ResponseStatus.USERNAME_REQUIRED_ERROR,
                     'password': ResponseStatus.PASSWORD_REQUIRED_ERROR,
                     'email': ResponseStatus.EMAIL_REQUIRED_ERROR
                     })
def register(request):
    # 经过处理的 JSON 数据
    json_data = request.json_data

    # 用户名 username 格式检验
    username = json_data['username']
    status = validate_username(username)
    if status is not None:
        request.status = status
        return process_response(request)

    # 密码 password 格式验证
    password = json_data['password']
    status = validate_password(password)
    if status is not None:
        request.status = status
        return process_response(request)

    # 邮箱 email 格式验证
    email = json_data['email']
    status = validate_email(email)
    if status is not None:
        request.status = status
        return process_response(request)

    # 用户名 username 存在性验证
    if account_models.User.objects.filter(username=username):
        request.status = ResponseStatus.USERNAME_EXISTED_ERROR
        return process_response(request)

    # 邮箱 email 存在性验证
    if account_models.UserInfo.objects.filter(email=email):
        request.status = ResponseStatus.EMAIL_EXISTED_ERROR
        return process_response(request)

    # 创建用户 user 和 用户信息 user_info
    user = account_models.User(username=username,
                               password=make_password(password)
                               )
    user.save()
    user_info = account_models.UserInfo(user=user,
                                        email=email
                                        )
    user_info.save()

    request.status = ResponseStatus.OK
    return process_response(request)


@RequiredMethod('POST')
@RequiredParameters({'username': ResponseStatus.USERNAME_REQUIRED_ERROR,
                     'password': ResponseStatus.PASSWORD_REQUIRED_ERROR,
                     })
def login(request):
    # 经过处理的 JSON 数据
    json_data = request.json_data

    username = json_data['username']
    password = json_data['password']

    # 用户 user 存在性验证
    user = account_models.User.objects.filter(username=username).first()
    if not user:
        request.status = ResponseStatus.USERNAME_NOT_EXISTED_ERROR
        return process_response(request)

    # 密码 password 验证
    if check_password(password, user.password) is False:
        request.status = ResponseStatus.PASSWORD_NOT_MATCH_ERROR
        return process_response(request)

    # 设置登陆状态
    request.session['username'] = username

    request.status = ResponseStatus.OK
    return process_response(request)
