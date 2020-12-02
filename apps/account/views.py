from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from ratelimit.decorators import ratelimit

from iBird import settings
from apps.utils.decorator import RequiredMethod, RequiredParameters, Protect
from apps.utils.response_status import ResponseStatus
from apps.utils.response_processor import process_response
from apps.utils.validator import validate_username, validate_password, validate_email
from apps.utils.random_string_generator import generate_string, Pattern
from apps.utils.email_sender import send
from apps.account import models as account_models


@Protect
@RequiredMethod('POST')
@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@RequiredParameters('username', 'password', 'email')
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


@Protect
@RequiredMethod('POST')
@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@RequiredParameters('username', 'password')
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


@Protect
@RequiredMethod('POST')
@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
def logout(request):
    if request.session.get('username') is not None:
        del request.session['username']
        status = ResponseStatus.OK
    else:
        status = ResponseStatus.NOT_LOGIN

    return process_response(request, status)


@Protect
@RequiredMethod('GET')
@ratelimit(**settings.RATE_LIMIT_LEVEL_3)
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


@Protect
@RequiredMethod('POST')
@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@RequiredParameters('username', 'password', 'new_password')
def change_password(request):
    json_data = request.json_data

    # 新密码 new_password 格式验证
    new_password = json_data['new_password']
    status = validate_password(new_password)
    if status is not None:
        return process_response(request, status)

    # 用户 user 存在性验证
    username = json_data['username']
    user = account_models.User.objects.filter(username=username).first()
    if not user:
        return process_response(request, ResponseStatus.USERNAME_NOT_EXISTED_ERROR)

    # 密码 password 验证
    password = json_data['password']
    if check_password(password, user.password) is False:
        return process_response(request, ResponseStatus.PASSWORD_NOT_MATCH_ERROR)

    # 修改密码 password
    user.password = make_password(new_password)
    user.save()

    return process_response(request, ResponseStatus.OK)


@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@RequiredParameters('username')
def send_password_verify_code(request):
    json_data = request.json_data

    # 用户 user 存在性验证
    username = json_data['username']
    user = account_models.User.objects.filter(username=username).first()
    if not user:
        return process_response(request, ResponseStatus.USERNAME_NOT_EXISTED_ERROR)

    # 生成随机数字验证码
    verify_code = generate_string(5, Pattern.Digits)

    # 填充邮件内容
    message = settings.VERIFY_CODE_MAIL_MESSAGE.format(code=verify_code, username=username)

    email = user.info.email
    send(email, message)

    # 将验证码存入缓存 10 min 过期
    cache.set('verify_code_' + email, verify_code, 10 * settings.MINUTE)

    return process_response(request, ResponseStatus.OK)


@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@RequiredParameters('username', 'new_password', 'verify_code')
def change_forget_password(request):
    json_data = request.json_data

    # 用户 user 存在性验证
    username = json_data['username']
    user = account_models.User.objects.filter(username=username).first()
    if not user:
        return process_response(request, ResponseStatus.USERNAME_NOT_EXISTED_ERROR)

    # 新密码 new_password 格式验证
    new_password = json_data['new_password']
    status = validate_password(new_password)
    if status is not None:
        return process_response(request, status)

    # 验证码匹配
    verify_code = json_data['verify_code']
    cached_code = cache.get('verify_code_' + user.info.email)
    if verify_code != cached_code:
        return process_response(request, ResponseStatus.VERIFY_CODE_NOT_MATCH_ERROR)

    # 修改密码 password
    user.password = make_password(new_password)
    user.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod(['POST', 'PATCH'])
def forget_password(request):
    return {'POST': send_password_verify_code, 'PATCH': change_forget_password}[request.method](request)
