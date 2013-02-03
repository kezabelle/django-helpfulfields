# -*- coding: utf-8 -*-
from django.db import models

class ChangeTracking(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
