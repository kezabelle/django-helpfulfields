# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models.query import QuerySet


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
