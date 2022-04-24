from django.db import models

# Create your models here.

class InwModel(models.Model):
    Nazwa = models.CharField(max_length=200, blank=True, null=True)
    EAN = models.IntegerField(blank=True, null=True)
    Ilosc = models.IntegerField()

    def __str__(self):
        return f'{self.Nazwa} {self.EAN} {self.Ilosc}'




