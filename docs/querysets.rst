Mixing model querysets
======================

.. include:: _references.rst

How to make use of them
-----------------------

The querysets represented herein are designed to be used with their
appropriate abstract models, and typically provide additional methods by
which to filter objects.

The obvious way to get these yourself is to create your own subclass which
implements them, and wire it up to a manager::

    from helpfulfields.querysets import (ChangeTrackingQuerySet,
                                         DatePublishingQuerySet,
                                         SoftDeleteQuerySet)

    class MyCustomQS(ChangeTrackingQuerySet, DatePublishingQuerySet, SoftDeleteQuerySet):
        pass

    class MyCustomManager(Manager):
        def get_query_set(self):
            return MyCustomQS(self.model)

        def created_recently(self, minutes=30):
            # this method is exposed via ChangeTrackingQuerySet
            return self.get_query_set().created_recently(minutes=minutes)

       #[...]

    class MyModel(Model):
        objects = MyCustomManager()

Avoiding the boilerplate
^^^^^^^^^^^^^^^^^^^^^^^^

Better than doing it all yourself though, is just to use a `PassThroughManager`
from `django-model-utils`_ to reduce the amount of repetition involved::

    from model_utils.managers import PassThroughManager
    from helpfulfields.querysets import (ChangeTrackingQuerySet,
                                         DatePublishingQuerySet,
                                         SoftDeleteQuerySet)

    class MyCustomQS(ChangeTrackingQuerySet, DatePublishingQuerySet, SoftDeleteQuerySet):
        pass

    class MyModel(Model):
        objects = PassThroughManager.for_queryset_class(MyCustomQS)()

The :mod:`querysets` available
------------------------------

.. automodule:: helpfulfields.querysets
    :members:
