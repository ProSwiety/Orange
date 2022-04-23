from django.db import models

# Create your models here.

class InwModel(models.Model):
    Nazwa = models.CharField(max_length=200)
    EAN = models.IntegerField()
    Ilosc = models.IntegerField()

    def __str__(self):
        return f'{self.Nazwa} {self.EAN} {self.Ilosc}'




