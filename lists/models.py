from statistics import mode
from django.db import models


# Create your models here.
class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List, on_delete=models.CASCADE, blank=False, null=False, default=5)
