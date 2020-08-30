from django.db import models

# Create your models here.


class URLToUniqueCode(models.Model):
    url = models.TextField('url', max_length=8192)
    unique_code = models.TextField('unique_code', unique=True)
    creation_time = models.DateTimeField('creation_time', auto_now_add=True)

    def __str__(self):
        return self.url

    class META:
        models.Model.ordering = ['creation_time']
