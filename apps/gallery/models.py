from django.db import models


class Photo(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, verbose_name='用户')
    path = models.CharField(max_length=100, verbose_name='图片路径', null=False, blank=False)
    report = models.ForeignKey('prediction.Report', on_delete=models.PROTECT, verbose_name='识别报告', null=True,
                               blank=True)
    address = models.CharField(max_length=255, verbose_name='地点', null=False, blank=True, default='')
    longitude = models.FloatField(verbose_name='经度', null=False, blank=True, default=0.0)
    latitude = models.FloatField(verbose_name='纬度', null=False, blank=True, default=0.0)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = verbose_name
