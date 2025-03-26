from django.db import models

# Create your models here.
class UrlData(models.Model):
    origin_url = models.URLField(max_length=2048,unique=True)
    hash = models.CharField(max_length=10, unique=True)
    expire_at = models.DateTimeField()

    def __str__(self):
        return self.origin_url