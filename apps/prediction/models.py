from django.db import models

from iBird import settings


class Report(models.Model):
    path = models.CharField(max_length=100, verbose_name='图片路径', null=False, blank=False)
    top1_label = models.CharField(max_length=50, verbose_name='TOP 1 名称')
    top2_label = models.CharField(max_length=50, verbose_name='TOP 2 名称')
    top3_label = models.CharField(max_length=50, verbose_name='TOP 3 名称')
    top4_label = models.CharField(max_length=50, verbose_name='TOP 4 名称')
    top5_label = models.CharField(max_length=50, verbose_name='TOP 5 名称')
    top1_label_index = models.IntegerField(verbose_name='TOP 1 标识')
    top2_label_index = models.IntegerField(verbose_name='TOP 2 标识')
    top3_label_index = models.IntegerField(verbose_name='TOP 3 标识')
    top4_label_index = models.IntegerField(verbose_name='TOP 4 标识')
    top5_label_index = models.IntegerField(verbose_name='TOP 5 标识')
    top1_probability = models.FloatField(verbose_name='TOP 1 概率')
    top2_probability = models.FloatField(verbose_name='TOP 2 概率')
    top3_probability = models.FloatField(verbose_name='TOP 3 概率')
    top4_probability = models.FloatField(verbose_name='TOP 4 概率')
    top5_probability = models.FloatField(verbose_name='TOP 5 概率')

    class Meta:
        verbose_name = '识别报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

    @property
    def sequence(self):
        return self.id

    def save(self, *args, **kwargs):
        if hasattr(self, 'result'):
            for i in range(1, 6):
                setattr(self, 'top' + str(i) + '_label', self.result[i - 1][0])
                setattr(self, 'top' + str(i) + '_label_index', self.result[i - 1][1])
                setattr(self, 'top' + str(i) + '_probability', self.result[i - 1][2])
        super().save(args, kwargs)

    def transform_into_serialized_data(self):
        return {
            'sequence': self.sequence,
            'path': self.path,
            'result': [
                {'label': self.top1_label, 'id': self.top1_label_index, 'probability': self.top1_probability,
                 'info': Bird.objects.filter(id=self.top1_label_index).first().info,
                 'img': settings.BIRDS_EXAMPLE_URL.format(bird_id=self.top1_label_index)
                 },
                {'label': self.top2_label, 'id': self.top2_label_index, 'probability': self.top2_probability,
                 'info': Bird.objects.filter(id=self.top2_label_index).first().info,
                 'img': settings.BIRDS_EXAMPLE_URL.format(bird_id=self.top2_label_index)
                 },
                {'label': self.top3_label, 'id': self.top3_label_index, 'probability': self.top3_probability,
                 'info': Bird.objects.filter(id=self.top3_label_index).first().info,
                 'img': settings.BIRDS_EXAMPLE_URL.format(bird_id=self.top3_label_index)
                 },
                {'label': self.top4_label, 'id': self.top4_label_index, 'probability': self.top4_probability,
                 'info': Bird.objects.filter(id=self.top4_label_index).first().info,
                 'img': settings.BIRDS_EXAMPLE_URL.format(bird_id=self.top4_label_index)
                 },
                {'label': self.top5_label, 'id': self.top5_label_index, 'probability': self.top5_probability,
                 'info': Bird.objects.filter(id=self.top5_label_index).first().info,
                 'img': settings.BIRDS_EXAMPLE_URL.format(bird_id=self.top5_label_index)
                 },
            ]
        }


class Bird(models.Model):
    name_CN = models.CharField(max_length=255, verbose_name='名称', null=False, blank=False)
    name_EN = models.CharField(max_length=255, verbose_name='名称', null=False, blank=False)
    info = models.TextField(verbose_name='介绍', null=False, blank=True)

    class Meta:
        verbose_name = '鸟类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name_CN

    def transform_into_serialized_data(self):
        return {
            'bird_id': self.id,
            'name': self.name_CN,
            'name_EN': self.name_EN,
            'info': self.info,
            'img': settings.BIRDS_EXAMPLE_URL.format(bird_id=self.id)
        }
