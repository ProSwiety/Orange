from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UploadModel(models.Model):
    name = models.CharField(max_length=50, null=False)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.date} {self.user}'


class InwModel(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    EAN = models.IntegerField(blank=True, null=True)
    quantity = models.IntegerField(default='1')
    upload = models.ForeignKey(UploadModel, on_delete=models.CASCADE, related_name='set')

    def __str__(self):
        return f'{self.name} {self.EAN} {self.quantity}'
