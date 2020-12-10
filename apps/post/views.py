from ratelimit.decorators import ratelimit
from django.core.paginator import Paginator
from django.db.models import Q

from iBird import settings
from apps.utils.decorator import RequiredMethod, RequiredParameters, Protect, LoginRequired
from apps.utils.response_status import ResponseStatus, ValueErrorStatus
from apps.utils.response_processor import process_response
from apps.account import models as account_models
from apps.gallery import models as gallery_models
from apps.post import models as post_models


@Protect
@RequiredMethod('POST')
@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@LoginRequired
@RequiredParameters('path', 'content')
def give_post(request):
    json_data = request.json_data

    status = ValueErrorStatus.check_value_type(json_data)
    if status is not None:
        return process_response(request, status)

    content = json_data['content']
    if len(content) > 400:
        return process_response(request, ResponseStatus.CONTENT_LENGTH_TOO_LARGE_ERROR)

    user = account_models.User.objects.filter(username=request.session.get('username')).first()
    path = json_data['path']
    photo = gallery_models.Photo.objects.filter(user=user, path=path).first()
    if not photo:
        return process_response(request, ResponseStatus.IMAGE_PATH_NOT_FOUND_ERROR)

    post = post_models.Post(user=user, photo=photo, content=content)
    post.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
@ratelimit(**settings.RATE_LIMIT_LEVEL_3)
def get_all_post(request):
    num = request.GET.get('num')
    if not num:
        num = 1
    else:
        status = ValueErrorStatus.check_value_type({'num': num})
        if status is not None:
            return process_response(request, status)
        num = int(num)

    posts = post_models.Post.objects.all().order_by('-id')

    paginator = Paginator(posts, settings.POST_PER_PAGE)
    total = paginator.num_pages

    if not 1 <= num <= total:
        return process_response(request, ResponseStatus.NUM_OUT_OF_RANGE_ERROR)

    page = paginator.page(num)

    user = request.session.get('username', None)
    if user is not None:
        user = account_models.User.objects.filter(username=user).first()

    post_list = []
    for one in page.object_list:
        post_list.append({
            'username': one.user.info.nickname if one.user.info.nickname else one.user.username,
            'avatar': one.user.info.avatar.url,
            'content': one.content,
            'create_time': one.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'address': one.photo.address,
            'like': one.like,
            'post_id': one.id
        })

        if user:
            post_list[-1]['is_liked'] = True if post_models.LikeRecord.objects.filter(user=user, post=one) else False

    request.data = {
        'post': post_list,
        'count': len(post_list),
        'num': num,
        'has_next': page.has_next()
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
@ratelimit(**settings.RATE_LIMIT_LEVEL_3)
def get_hot_post(request):
    posts = post_models.Post.objects.all().order_by('like', '-id')[:10]

    user = request.session.get('username', None)
    if user is not None:
        user = account_models.User.objects.filter(username=user).first()

    post_list = []
    for one in posts:
        post_list.append({
            'username': one.user.info.nickname if one.user.info.nickname else one.user.username,
            'avatar': one.user.info.avatar.url,
            'content': one.content,
            'create_time': one.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'address': one.photo.address,
            'like': one.like,
            'post_id': one.id
        })

        if user:
            post_list[-1]['is_liked'] = True if post_models.LikeRecord.objects.filter(user=user, post=one) else False

    request.data = {
        'post': post_list,
        'count': len(post_list)
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
@ratelimit(**settings.RATE_LIMIT_LEVEL_3)
@LoginRequired
def get_my_post(request):
    num = request.GET.get('num')
    if not num:
        num = 1
    else:
        status = ValueErrorStatus.check_value_type({'num': num})
        if status is not None:
            return process_response(request, status)
        num = int(num)

    user = account_models.User.objects.filter(username=request.session.get('username')).first()
    posts = post_models.Post.objects.filter(user=user).order_by('-id')

    paginator = Paginator(posts, settings.POST_PER_PAGE)
    total = paginator.num_pages

    if not 1 <= num <= total:
        return process_response(request, ResponseStatus.NUM_OUT_OF_RANGE_ERROR)

    page = paginator.page(num)

    post_list = []
    for one in page.object_list:
        post_list.append({
            'username': one.user.info.nickname if one.user.info.nickname else one.user.username,
            'avatar': one.user.info.avatar.url,
            'content': one.content,
            'create_time': one.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'address': one.photo.address,
            'like': one.like,
            'post_id': one.id
        })

        if user:
            post_list[-1]['is_liked'] = True if post_models.LikeRecord.objects.filter(user=user, post=one) else False

    request.data = {
        'post': post_list,
        'count': len(post_list),
        'num': num,
        'has_next': page.has_next()
    }

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('POST')
@ratelimit(**settings.RATE_LIMIT_LEVEL_2)
@LoginRequired
@RequiredParameters('post_id')
def like_post(request):
    json_data = request.json_data

    status = ValueErrorStatus.check_value_type(json_data)
    if status is not None:
        return process_response(request, status)

    post_id = json_data['post_id']
    post = post_models.Post.objects.filter(id=post_id).first()
    if not post:
        return process_response(request, ResponseStatus.POST_NOT_FOUND_ERROR)

    user = account_models.User.objects.filter(username=request.session.get('username')).first()
    if post_models.LikeRecord.objects.filter(user=user, post=post):
        return process_response(request, ResponseStatus.LIKE_ALREADY_ERROR)

    post.like += 1
    post.save()

    like = post_models.LikeRecord(user=user, post=post)
    like.save()

    return process_response(request, ResponseStatus.OK)


@Protect
@RequiredMethod('GET')
@ratelimit(**settings.RATE_LIMIT_LEVEL_3)
def get_points(request):
    posts = post_models.Post.objects.filter(~(Q(photo__address='') | Q(photo__report=None)))

    point = []
    for one in posts:
        point.append({
            'content': one.content,
            'address': one.photo.address,
            'longitude': one.photo.longitude,
            'latitude': one.photo.latitude
        })

    request.data = {
        'point': point,
        'count': len(point)
    }

    return process_response(request, ResponseStatus.OK)
