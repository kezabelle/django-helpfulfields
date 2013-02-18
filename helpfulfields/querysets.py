# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models.query import QuerySet

# The querysets represented herein are designed to be used with their
# approrpriate abstract models, and typically provide additional methods by
# which to filter objects. The simplest way to get these yourself is to
# create your own subclass which implements them, and wire it up to a manager.
# .. code::
#
# class MyCustomQS(ChangeTrackingQuerySet, DatePublishingQuerySet, SoftDeleteQuerySet)
#   pass
#
# class MyCustomerManager(Manager):
#   def get_query_set(self):
#       return MyCustomQS(self.model)

#   def created_recently(self, minutes=30):
#       return self.get_query_set().created_recently(minutes=minutes)
#
# Better than that though, is just to use `django-model-utils`
# .. code::
#
# from model_utils.managers import PassThroughManager
#
# class MyModel(Model):
#   objects = PassThroughManager.for_queryset_class(MyCustomQS)()


class ChangeTrackingQuerySet(QuerySet):
    """
    A custom queryset for filtering things using the `Publishing` Abstract model
    via it's boolean.
    Recommended to be used by mixing together querysets and using
    `django-model-utils` to make a Passthrough manager.
    """
    def created_recently(self, minutes=30):
        """Goes hand in hand with the `created_recently` method. Finds all
        object instances created within the last N minutes.

        :return: filtered objects
        :rtype: :class:QuerySet
        """
        recently = datetime.now() - timedelta(minutes=minutes)
        return self.filter(created__gte=recently)

    def modified_recently(self, minutes=30):
        """Goes hand in hand with the `modified_recently` method. Finds all
        object instances modified within the last N minutes.

        :return: filtered objects
        :rtype: :class:QuerySet
        """
        recently = datetime.now() - timedelta(minutes=minutes)
        return self.filter(modified__gte=recently)


class PublishingQuerySet(QuerySet):
    """
    A custom queryset for filtering things using the `Publishing` Abstract model
    via it's boolean.
    Recommended to be used by mixing together querysets and using
    `django-model-utils` to make a Passthrough manager.
    """
    def published(self):
        return self.filter(is_published=True)

    def unpublished(self):
        return self.filter(is_published=False)


class DatePublishingQuerySet(QuerySet):
    """
    A custom queryset for filtering things using the `Publishing` Abstract model
    via it's boolean.
    Recommended to be used by mixing together querysets and using
    `django-model-utils` to make a Passthrough manager.
    """
    def published(self):
        """
        Find all objects who have an end publishing date in the future, or no
        end date, and ALSO have a publish date in the past or present.
        :return: All published objects
        :rtype: :class:QuerySet subclass
        """
        now = datetime.now()
        maybe_published = Q(unpublish_on__gte=now) | Q(unpublish_on__isnull=True)
        definitely_published = Q(publish_on__lte=now)
        return self.filter(maybe_published & definitely_published)

    def unpublished(self):
        """
        Find all objects who have an end publishing date in the past, OR a start
        date in the future.
        :return: All unpublished objects
        :rtype: :class:QuerySet subclass
        """
        now = datetime.now()
        return self.filter(Q(unpublish_on__lte=now) | Q(publish_on__gte=now))


class SoftDeleteQuerySet(QuerySet):
    """
    A custom queryset which goes hand in hand with the `SoftDelete` model to
    provide a way to filter by the additional field that creates.
    """

    def all(self):
        """ Finds all objects which haven't been marked as deleted. This
        includes those which have been restored previously.
        :return: objects which haven't been marked as deleted
        :rtype: :class:QuerySet
        """
        restored_val = self.model.DELETED_CHOICES[1][0]
        return super(SoftDeleteQuerySet, self).all().filter(
            Q(deleted__isnull=True) | Q(deleted=restored_val)
        )

    def deleted(self):
        """ filters the queryset looking for deleted items only.
        :return: objects which are currently deleted
        :rtype: :class:QuerySet
        """
        deleted_val = self.model.DELETED_CHOICES[2][0]
        return self.filter(deleted=deleted_val)

    def restored(self):
        """ filters the queryset looking for objects which have been previously
        deleted, and since restored.
        :return: objects which were once deleted.
        :rtype: :class:QuerySet
        """
        restored_val = self.model.DELETED_CHOICES[1][0]
        return self.filter(deleted=restored_val)


