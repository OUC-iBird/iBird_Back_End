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
        return process_response(request, status)

    # 密码 password 格式验证
    password = json_data['password']
    status = validate_password(password)
    if status is not None:
        return process_response(request, status)

    # 邮箱 email 格式验证
    email = json_data['email']
    status = validate_email(email)
    if status is not None:
        return process_response(request, status)

    # 用户名 username 存在性验证
    if account_models.User.objects.filter(username=username):
        return process_response(request, ResponseStatus.USERNAME_EXISTED_ERROR)

    # 邮箱 email 存在性验证
    if account_models.UserInfo.objects.filter(email=email):
        return process_response(request, ResponseStatus.EMAIL_EXISTED_ERROR)

    # 创建用户 user 和 用户信息 user_info
    user = account_models.User(username=username,
                               password=make_password(password)
                               )
    user.save()
    user_info = account_models.UserInfo(user=user,
                                        email=email
                                        )
    user_info.save()

    return process_response(request, ResponseStatus.OK)


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
        return process_response(request, ResponseStatus.USERNAME_NOT_EXISTED_ERROR)

    # 密码 password 验证
    if check_password(password, user.password) is False:
        return process_response(request, ResponseStatus.PASSWORD_NOT_MATCH_ERROR)

    # 设置登陆状态
    request.session['username'] = username

    return process_response(request, ResponseStatus.OK)


@RequiredMethod('POST')
def logout(request):
    if request.session.get('username') is not None:
        del request.session['username']
        status = ResponseStatus.OK
    else:
        status = ResponseStatus.NOT_LOGIN

    return process_response(request, status)


@RequiredMethod('GET')
def get_status(request):
    if request.session.get('username') is not None:
        username = request.session.get('username')

        user = account_models.User.objects.filter(username=username).first()
        if not user:
            return process_response(request, ResponseStatus.UNEXPECTED_ERROR)

        request.data = {
            'login': True,
            'username': user.username,
            'nickname': user.info.nickname,
            'avatar': user.info.avatar.url,
        }

        return process_response(request, ResponseStatus.OK)
    else:
        request.data = {
            'login': False,
        }

        return process_response(request, ResponseStatus.OK)
