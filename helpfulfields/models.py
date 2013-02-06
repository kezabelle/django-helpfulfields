# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db import models
from helpfulfields.text import (seo_title_label, seo_title_help,
                                seo_description_label, seo_description_help,
                                seo_keywords_label, seo_keywords_help,
                                soft_delete_label, soft_delete_help,
                                soft_delete_initial, soft_delete_false,
                                soft_delete_true, titles_title_label,
                                titles_menu_label, titles_menu_help, publish_label,
                                publish_help, unpublish_label, unpublish_help,
                                quick_publish_label, quick_publish_help)


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



class SEO(models.Model):
    """Abstract model for extending custom models with SEO fields

    Attempts to maintain compatibility with django CMS, in terms of access methods,
    but not underlying objects  (as django CMS has Title objects).

    """
    meta_title = models.CharField(max_length=255, blank=True, null=False,
        verbose_name=seo_title_label, help_text=seo_title_help)
    meta_description = models.TextField(max_length=255, blank=True, null=False,
        verbose_name=seo_description_label, help_text=seo_description_help)
    meta_keywords = models.CharField(max_length=255, blank=True, null=False,
        verbose_name=seo_keywords_label, help_text=seo_keywords_help)

    def get_page_title(self):
        """ utility method for django CMS api compatibility """
        return self.meta_title

    def get_meta_description(self):
        """ utility method for django CMS api compatibility """
        return self.meta_description

    def get_meta_keywords(self):
        """ utility method for django CMS api compatibility """
        return self.meta_keywords

    class Meta:
        abstract = True



class Publishing(models.Model):
    is_published = models.BooleanField(default=False, verbose_name=quick_publish_label,
        help_text=quick_publish_help)

    class Meta:
        abstract = True



class DatePublishing(models.Model):
    publish_on = models.DateTimeField(default=datetime.now,
        verbose_name=publish_label, help_text=publish_help)
    unpublish_on = models.DateTimeField(default=None, blank=True, null=True,
        verbose_name=unpublish_label, help_text=unpublish_help)

    def is_published(self):
        now = datetime.now()
        if self.unpublish_on is not None:
            return self.unpublish_on >= now and self.publish_on <= now
        else:
            return self.publish_on <= now
        return False

    class Meta:
        abstract = True


class SoftDelete(models.Model):
    DELETED_CHOICES = (
        (None, soft_delete_initial),
        (False, soft_delete_false),
        (True, soft_delete_true)
        )
    soft_delete = models.NullBooleanField(default=DELETED_CHOICES[0][0],
        choices=DELETED_CHOICES, verbose_name=soft_delete_label,
        help_text=soft_delete_help)

    class Meta:
        abstract = True
