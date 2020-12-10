from django.db import models


class Post(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, verbose_name='用户')
    photo = models.ForeignKey('gallery.Photo', on_delete=models.PROTECT, verbose_name='图片')
    content = models.CharField(max_length=400, verbose_name='内容', null=False, blank=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    like = models.BigIntegerField(verbose_name='点赞数', default=0)

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = verbose_name


class LikeRecord(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, verbose_name='用户')
    post = models.ForeignKey('post.Post', on_delete=models.PROTECT, verbose_name='动态')

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
