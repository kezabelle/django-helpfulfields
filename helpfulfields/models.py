# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from helpfulfields.settings import RECENTLY_MINUTES
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


class ChangeTracking(models.Model):
    """
    Abstract model for extending custom models with an audit of when things were
    changed. By extension, allows us to use get_latest_by to establish the most
    recent things.

    .. note::
        It transpires that this is basically an accidental rewrite of
        `django-model-utils`_ TimeStampedModel, though it provides a few
        extra bits.
    """

    #: a :mod:`datetime.datetime` representing the original date this
    #: object was saved. Represented as a
    #: :class:`~django.db.models.DateTimeField`.
    created = models.DateTimeField(auto_now_add=True, verbose_name=created_label,
                                   help_text=created_help)

    #: a :mod:`datetime.datetime` representing the last time this
    #: object was changed. Represented as a
    #: :class:`~django.db.models.DateTimeField`.
    modified = models.DateTimeField(auto_now=True, verbose_name=modified_label,
                                    help_text=modified_help)

    def created_recently(self, **kwargs):
        """
        Was this object created recently?
        Accepts a list of `kwargs` which are passed directly to
        :func:`~datetime.timedelta`; in the absence of any `kwargs` the timedelta
        is told 30 minutes is recent.

        :return: whether or not this object was recently created
        :rtype: boolean
        """
        # Default to 30 minutes, as per previous implementation.
        if len(kwargs.keys()) == 0:
            kwargs.update(minutes=RECENTLY_MINUTES)
        if not self.created:
            return False
        recently = datetime.now() - timedelta(**kwargs)
        return self.created >= recently

    def modified_recently(self, **kwargs):
        """
        Was this object changed recently?
        Accepts a list of `kwargs` which are passed directly to
        :func:`~datetime.timedelta`; in the absence of any `kwargs` the timedelta
        is told 30 minutes is recent.

        :return: whether or not this object was recently changed.
        :rtype: boolean
        """
        # Default to 30 minutes, as per previous implementation.
        if len(kwargs.keys()) == 0:
            kwargs.update(minutes=RECENTLY_MINUTES)
        if not self.modified:
            return False
        recently = datetime.now() - timedelta(**kwargs)
        return self.modified >= recently

    class Meta:
        abstract = True


class Titles(models.Model):
    """ Abstract model for providing a title + menu title field.

    Also supplies a get_menu_title method, which falls back to the title if no
    menu title is set.
    """

    #: Required :class:`~django.db.models.CharField` for an object,
    #: whose `max_length` is *255*.
    title = models.CharField(max_length=255, verbose_name=titles_title_label)

    #: Optional :class:`~django.db.models.CharField` for an object,
    #: whose `max_length` is *255*, and may be used to represent this
    #: object in menus.
    menu_title = models.CharField(max_length=255, blank=True,
                                  verbose_name=titles_menu_label,
                                  help_text=titles_menu_help)

    def get_menu_title(self):
        """ utility method for `django CMS`_ api compatibility

        :return: the `menu_title`, or if not set, the `title`
        :rtype: unicode string
        """
        if self.menu_title:
            return self.menu_title
        return self.title

    class Meta:
        abstract = True


class SEO(models.Model):
    """Abstract model for extending custom models with SEO fields

    Attempts to maintain compatibility with `django CMS`_, in terms of access
    methods, but not underlying objects  (as `django CMS`_ has Title objects).
    """

    #: a :class:`~django.db.models.CharField` for storing the page's
    #: title. Defined with a `max_length` of *255*.
    meta_title = models.CharField(max_length=255, blank=True, null=False,
                                  verbose_name=seo_title_label,
                                  help_text=seo_title_help)

    #: a :class:`~django.db.models.CharField` for storing the description
    #: sometimes used in Search Engines. Defined with a `max_length` of *255*.
    meta_description = models.TextField(max_length=255, blank=True, null=False,
                                        verbose_name=seo_description_label,
                                        help_text=seo_description_help)

    #: a :class:`~django.db.models.CharField` for storing a bunch of keywords.
    #: Not used by many (any?) Search engines now, but provided for historical
    #: completeness, and API compatibility with `django CMS`_. Defined with a
    #: `max_length` of *255*.
    meta_keywords = models.CharField(max_length=255, blank=True, null=False,
                                     verbose_name=seo_keywords_label,
                                     help_text=seo_keywords_help)

    def get_page_title(self):
        """ utility method for `django CMS`_ api compatibility

        :return: the `meta_title` field's value
        :rtype: unicode string
        """
        return self.meta_title

    def get_meta_description(self):
        """ utility method for `django CMS`_ api compatibility

        :return: the `meta_description` field's value
        :rtype: unicode string
        """
        return self.meta_description

    def get_meta_keywords(self):
        """ utility method for `django CMS`_ api compatibility

        :return: the `meta_description` field's value
        :rtype: unicode string
        """
        return self.meta_keywords

    class Meta:
        abstract = True


class Publishing(models.Model):
    """
    For when you don't need date based publishing (using :class:`DatePublishing`)
    this abstract model provides the same API.

    For better results, this should be combined with
    :class:`~helpfulfields.querysets.PublishingQuerySet`.
    """

    #: :class:`~django.db.models.BooleanField` deciding whether or not the
    #: object is available on the site. Defaults to `False`.
    is_published = models.BooleanField(default=False,
                                       verbose_name=quick_publish_label,
                                       help_text=quick_publish_help)

    class Meta:
        abstract = True


class DatePublishing(models.Model):
    """ A perennial favourite, publish start and end dates, as an abstract model.

    Has the same `is_published` attribute that :class:`Publishing` has.

    For querying, this should be combined with
    :class:`~helpfulfields.querysets.DatePublishingQuerySet`.
    """

    #: Defaults to :py:mod:`datetime.datetime.now()` - the date on which this
    #: should be available on the site. Represented as a
    #: :class:`~django.db.models.DateTimeField`.
    publish_on = models.DateTimeField(default=datetime.now,
                                      verbose_name=publish_label,
                                      help_text=publish_help)

    #: the date on which this should expire from the site. Represented as
    #: a :class:`~django.db.models.DateTimeField`.
    unpublish_on = models.DateTimeField(default=None, blank=True, null=True,
                                        verbose_name=unpublish_label,
                                        help_text=unpublish_help)

    @property
    def is_published(self):
        """
        For API compatibility with the alternate publishing model
        :class:`Publishing` which uses a boolean property, this method is
        accessed the same way, and is decorated with `@property` for this reason.

        :return: Whether or not this object is currently visible
        :rtype: boolean
        """
        now = datetime.now()
        if self.unpublish_on is not None:
            # maybe self.unpublish_on >= now >= self.publish_on ???
            return self.unpublish_on >= now and self.publish_on <= now
        else:
            return self.publish_on <= now

    class Meta:
        abstract = True


class SoftDelete(models.Model):
    """ I've not actually used this yet. It's just a sketch of something I'd like.

    The idea is that nothing should ever really be deleted, but I have no idea
    how feasible this is at an abstract level.

    .. warning::
        This should not be relied on to prevent data loss, as it is very much
        an incomplete idea right now.

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
        """
        Instead of deleting this object, and all it's related items,
        we hide remove it softly. This means that currently there will be a lot
        of pseudo-orphans, because I've not yet decided on how to handle them.
        They're just hangers-on, really.

        :param using: the db router to use.
        :rtype: None
        """
        assert self._get_pk_val() is not None, object_lacks_pk % {
            'model': self._meta.object_name,
            'pk': self._meta.pk.attname
        }
        self.deleted = self.DELETED_CHOICES[2][0]
        self.save(using=using)
    delete.alters_data = True

    def restore(self, using=None):
        """
        Converts a previously deleted object to it's restored state, by switching
        the value in the boolean to False (as opposed to NULL for never-deleted)

        :param using: the db router to use.
        :rtype: None
        """
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
