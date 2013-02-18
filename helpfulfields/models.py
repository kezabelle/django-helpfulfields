# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from helpfulfields.text import (seo_title_label, seo_title_help,
                                seo_description_label, seo_description_help,
                                seo_keywords_label, seo_keywords_help,
                                soft_delete_label, soft_delete_help,
                                soft_delete_initial, soft_delete_false,
                                soft_delete_true, titles_title_label,
                                titles_menu_label, titles_menu_help,
                                publish_label, publish_help, unpublish_label,
                                unpublish_help, quick_publish_label,
                                quick_publish_help, object_lacks_pk,
                                object_not_deleted, created_label, created_help,
                                modified_label, modified_help)
from helpfulfields.utils import datediff


class ChangeTracking(models.Model):
    """
    Abstract model for extending custom models with an audit of when things were
    changed. By extension, allows us to use get_latest_by to establish the most
    recent things.

    .. note::
        It transpires that this is basically an accidental rewrite of
        `django-model-utils` :class:TimeStampedModel, though it provides a few
        extra bits.
    """
    created = models.DateTimeField(auto_now_add=True, verbose_name=created_label,
                                   help_text=created_help)
    modified = models.DateTimeField(auto_now=True, verbose_name=modified_label,
                                    help_text=modified_help)

    def created_recently(self, minutes=30):
        return datediff(self.modified, minutes=minutes)

    def modified_recently(self, minutes=30):
        return datediff(self.modified, minutes=minutes)

    class Meta:
        abstract = True


class Titles(models.Model):
    """ Abstract model for providing a title + menu title field.

    Also supplies a get_menu_title method, which falls back to the title if no
    menu title is set.
    """
    title = models.CharField(max_length=255, verbose_name=titles_title_label)
    menu_title = models.CharField(max_length=255, blank=True,
                                  verbose_name=titles_menu_label,
                                  help_text=titles_menu_help)

    def get_menu_title(self):
        """ utility method for django CMS api compatibility """
        if self.menu_title:
            return self.menu_title
        return self.title

    class Meta:
        abstract = True


class SEO(models.Model):
    """Abstract model for extending custom models with SEO fields

    Attempts to maintain compatibility with django CMS, in terms of access
    methods, but not underlying objects  (as django CMS has Title objects).

    """
    meta_title = models.CharField(max_length=255, blank=True, null=False,
                                  verbose_name=seo_title_label,
                                  help_text=seo_title_help)
    meta_description = models.TextField(max_length=255, blank=True, null=False,
                                        verbose_name=seo_description_label,
                                        help_text=seo_description_help)
    meta_keywords = models.CharField(max_length=255, blank=True, null=False,
                                     verbose_name=seo_keywords_label,
                                     help_text=seo_keywords_help)

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
    """
    For when you don't need date based publishing, this abstract model
    provides the same API.
    """
    is_published = models.BooleanField(default=False,
                                       verbose_name=quick_publish_label,
                                       help_text=quick_publish_help)

    class Meta:
        abstract = True


class DatePublishing(models.Model):
    """ A perennial favourite, publish start and end dates, as an abstract model.

    Has the same `is_published` attribute that `Publishing` has.
    """
    publish_on = models.DateTimeField(default=datetime.now,
                                      verbose_name=publish_label,
                                      help_text=publish_help)
    unpublish_on = models.DateTimeField(default=None, blank=True, null=True,
                                        verbose_name=unpublish_label,
                                        help_text=unpublish_help)

    @property
    def is_published(self):
        """
        Method which behaves as a property, for API stability with `Publishing`

        :return: Whether or not this object is currently visible
        :rtype: boolean
        """
        now = datetime.now()
        if self.unpublish_on is not None:
            return self.unpublish_on >= now and self.publish_on <= now
        else:
            return self.publish_on <= now
        return False

    class Meta:
        abstract = True


class SoftDelete(models.Model):
    """ I've not actually used this yet. It's just a sketch of something I'd like.

    The idea is that nothing should ever really be deleted, but I have no idea
    how feasible this is at an abstract level.
    """
    DELETED_CHOICES = (
        (None, soft_delete_initial),
        (False, soft_delete_false),
        (True, soft_delete_true)
    )
    deleted = models.NullBooleanField(default=DELETED_CHOICES[0][0],
                                      choices=DELETED_CHOICES,
                                      verbose_name=soft_delete_label,
                                      help_text=soft_delete_help)

    def delete(self, using=None):
        """Instead of deleting this object, and all it's related items,
        we hide remove it softly. This means that currently there will be a lot
        of pseudo-orphans, because I've not yet decided on how to handle them.
        They're just hangers-on, really.
        """
        assert self._get_pk_val() is not None, object_lacks_pk % {
            'model': self._meta.object_name,
            'pk': self._meta.pk.attname
        }
        self.deleted = self.DELETED_CHOICES[2][0]
        self.save(using=using)
    delete.alters_data = True

    def restore(self, using=None):
        for_assertions = {
            'model': self._meta.object_name,
            'pk': self._meta.pk.attname
        }
        assert self._get_pk_val() is not None, object_lacks_pk % for_assertions
        assert self.deleted == self.DELETED_CHOICES[2][0], object_not_deleted % for_assertions
        self.deleted = self.DELETED_CHOICES[1][0]
        self.save(using=using)

    class Meta:
        abstract = True


class Generic(models.Model):
    """
    For handling generic relations in a uniform way (assuming that only 1 is
    required on the subclassing model).

      * Doesn't provide a related_name from ContentType back to the subclass.
      * Uses a CharField for the content_id, so that apps may have non-integer
        primary keys (eg: uuid4())
    """
    content_type = models.ForeignKey(ContentType, related_name='+')
    content_id = models.CharField(max_length=255, db_index=True)
    content_object = GenericForeignKey('content_type', 'content_id')

    class Meta:
        abstract = True
