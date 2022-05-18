from django.db import models


class Measurement(models.Model):
    name = models.CharField(max_length=100, blank=False)
