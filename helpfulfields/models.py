# -*- coding: utf-8 -*-
from django.db import models

class ChangeTracking(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Titles(models.Model):
    title = models.CharField(max_length=255, verbose_name=titles_title_label)
    menu_title = models.CharField(max_length=255, blank=True,
        verbose_name=titles_menu_label, help_text=titles_menu_help)

    def get_menu_title(self):
        if self.menu_title:
            return self.menu_title
        return self.title

    class Meta:
        abstract = True

