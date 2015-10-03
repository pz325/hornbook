from django.db import models
from django.contrib import admin


class Hanzi(models.Model):
    """Study record saves"""
    content = models.CharField(max_length=6, primary_key=True)


admin.site.register(Hanzi)
