from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30, verbose_name='用户名', unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, verbose_name='密码', null=False, blank=False)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @property
    def info(self):
        return UserInfo.objects.filter(user=self)[0]


class UserInfo(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='用户')
    nickname = models.CharField(max_length=50, verbose_name='昵称', null=False, blank=True, default='')
    email = models.EmailField(verbose_name='邮箱', unique=True, null=False, blank=False)
    avatar = models.ImageField(upload_to='avatar', verbose_name='头像', default='/avatar/default.jpg')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
