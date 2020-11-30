from django.db import models


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
        return self.id

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
                (self.top1_label, self.top1_label_index, self.top1_probability),
                (self.top2_label, self.top2_label_index, self.top2_probability),
                (self.top3_label, self.top3_label_index, self.top3_probability),
                (self.top4_label, self.top4_label_index, self.top4_probability),
                (self.top5_label, self.top5_label_index, self.top5_probability),
            ]
        }
