# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from uuid import uuid4
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.util import flatten_fieldsets
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase as DjangoTestCase
from django.utils.encoding import force_unicode
from django.utils.unittest import TestCase as UnitTestCase
from helpfulfields.admin import (ViewOnSite, LogEntrySparkline, RelationCount,
                                 RelationList, changetracking_fieldset,
                                 titles_fieldset, publishing_fieldset,
                                 date_publishing_fieldset, seo_fieldset)
from helpfulfields.models import (ChangeTracking, Titles, SEO, Publishing,
                                  DatePublishing)
from helpfulfields.querysets import (ChangeTrackingQuerySet, PublishingQuerySet,
                                     DatePublishingQuerySet)
from helpfulfields.settings import RECENTLY_MINUTES, MAX_NUM_RELATIONS
from helpfulfields.text import logentry_empty
from model_utils.managers import PassThroughManager


class TestModelQuerySet(ChangeTrackingQuerySet, PublishingQuerySet):
    pass


class TestModel(ChangeTracking, Titles, SEO, Publishing):
    objects = PassThroughManager.for_queryset_class(TestModelQuerySet)()
    changes = PassThroughManager.for_queryset_class(ChangeTrackingQuerySet)()
    publishing = PassThroughManager.for_queryset_class(PublishingQuerySet)()

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u'/whee/'


class TestModelDates(Titles, DatePublishing):
    objects = PassThroughManager.for_queryset_class(DatePublishingQuerySet)()


class ChangeTrackingTestCase(DjangoTestCase):
    """
    Should verify all the methods and attributes provided by something
    inheriting from ChangeTracking work correctly
    """
    def test_object_methods(self):
        """
        Make sure that the `created_recently` and `modified_recently` model
        methods work as expected
        """
        old_date = datetime.now() - timedelta(days=1)
        obj = TestModel(title="changetracking_methods")
        self.assertFalse(obj.created_recently())
        self.assertFalse(obj.modified_recently())
        obj.save()
        self.assertTrue(obj.created_recently())
        self.assertTrue(obj.modified_recently())

        obj.created = old_date
        obj.modified = old_date

        self.assertFalse(obj.created_recently())
        self.assertFalse(obj.modified_recently())

        # test custom timedeltas
        self.assertTrue(obj.created_recently(days=2))
        self.assertTrue(obj.modified_recently(days=2))

    def test_manager_methods(self):
        """
        Make sure that the `created_recently` and `modified_recently` queryset
        methods work as expected
        """
        old_date = datetime.now() - timedelta(days=1)
        # Test both the base queryset, and the one that is mixed together.
        for manager in (TestModel.objects, TestModel.changes):
            obj = TestModel(title="changetracking_queryset_methods")
            obj.save()
            created = manager.created_recently().values_list('pk', flat=True)
            modified = manager.modified_recently().values_list('pk', flat=True)
            self.assertEqual([obj.pk], list(created))
            self.assertEqual([obj.pk], list(modified))

            obj.created = old_date
            obj.save()
            created = manager.created_recently().values_list('pk', flat=True)
            self.assertEqual([], list(created))

            # we can't use the save method, because it'll set the modified time.
            # by using queryset update, we can do it!
            manager.all().update(modified=old_date)
            modified = manager.modified_recently().values_list('pk', flat=True)
            self.assertEqual([], list(modified))

            # the same tests, but using custom timedeltas.
            created = manager.created_recently(days=2).values_list('pk', flat=True)
            modified = manager.modified_recently(days=2).values_list('pk', flat=True)
            self.assertEqual([obj.pk], list(created))
            self.assertEqual([obj.pk], list(modified))

            self.assertIsNone(obj.delete())


class PublishingTestCase(DjangoTestCase):

    def test_has_attribute(self):
        """
        make sure our mixed together model gets the right attribute
        """
        obj = TestModel(title='publishing_has_attr')
        obj.is_published = True
        obj.save()
        obj.delete()

    def test_manager_methods(self):
        """
        Make sure the queryset methods are exposed to the manager, and do the
        right thing.
        """
        for manager in (TestModel.objects, TestModel.publishing):
            obj = TestModel(title='publishing_is_published')
            obj.is_published = True
            obj.save()

            obj2 = TestModel(title='publishing_isnt_published')
            obj2.is_published = False
            obj2.save()
            manager = manager.order_by('pk')
            pubs = manager.published().values_list('pk', flat=True)
            unpubs = manager.unpublished().values_list('pk', flat=True)
            self.assertEqual([obj.pk], list(pubs))
            self.assertEqual([obj2.pk], list(unpubs))

            # check that changing status does the right thing.
            obj2.is_published = True
            obj2.save()
            pubs = manager.published().values_list('pk', flat=True)
            unpubs = manager.unpublished().values_list('pk', flat=True)
            self.assertEqual([obj.pk, obj2.pk], list(pubs))
            self.assertEqual([], list(unpubs))

            obj.delete()
            obj2.delete()


class DatePublishingTestCase(DjangoTestCase):
    def test_has_attribute(self):
        """
        make sure our mixed together model gets the right attribute
        """
        obj = TestModel(title='date_publishing_has_attr')
        obj.save()
        self.assertFalse(obj.is_published)

    def test_publishing(self):
        old_date = datetime.now() - timedelta(minutes=1)
        obj = TestModelDates(title='date_publishing_is_published')
        obj.publish_on = old_date
        obj.unpublish_on = None
        obj.save()

        self.assertTrue(obj.is_published)

        pubs = TestModelDates.objects.published().values_list('pk', flat=True)
        unpubs = TestModelDates.objects.unpublished().values_list('pk', flat=True)
        self.assertEqual([obj.pk], list(pubs))
        self.assertEqual([], list(unpubs))

        obj.unpublish_on = old_date
        obj.save()
        pubs = TestModelDates.objects.published().values_list('pk', flat=True)
        unpubs = TestModelDates.objects.unpublished().values_list('pk', flat=True)
        self.assertEqual([], list(pubs))
        self.assertEqual([obj.pk], list(unpubs))

    def test_unpublish_method(self):
        old_date = datetime.now() - timedelta(minutes=1)
        obj = TestModelDates(title='date_publishing_is_published')
        obj.publish_on = old_date
        obj.unpublish_on = None
        obj.save()
        self.assertTrue(obj.is_published)
        obj.unpublish()
        self.assertFalse(obj.is_published)
        # unpublishing something which is already unpublished should raise
        # an error.
        self.assertRaises(AssertionError, lambda: obj.unpublish())

    def test_is_published_api(self):
        obj = TestModelDates(title='date_publishing_is_published')
        obj.is_published = False
        obj.save()
        self.assertFalse(obj.is_published)
        self.assertLess(obj.publish_on, datetime.now())
        self.assertLess(obj.unpublish_on, datetime.now())

        obj.is_published = True
        obj.save()
        self.assertTrue(obj.is_published)
        self.assertLess(obj.publish_on, datetime.now())
        self.assertIsNone(obj.unpublish_on)


class TitlesTestCase(DjangoTestCase):

    def test_menutitle_method(self):
        """
        test the `get_menu_title` method, and force coverage.
        """
        title = u'titles_no_menu_title'
        mtitle = u'titles_now_with_menu_title'
        obj = TestModel(title=title)
        obj.save()
        self.assertEqual(title, obj.get_menu_title())
        obj.menu_title = mtitle
        obj.save()
        self.assertNotEqual(title, obj.get_menu_title())
        self.assertEqual(mtitle, obj.get_menu_title())


class SEOTestCase(DjangoTestCase):
    def test_provided_methods(self):
        """
        test the `get_menu_title` method, and force coverage.
        """
        title = u'titles_no_meta_title'
        mtitle = u'titles_page_meta_title'
        mkeys = u'keywords!'
        mdesc = u'a meta description!'
        obj = TestModel(title=title)
        obj.save()
        self.assertEqual(u'', obj.get_page_title())
        self.assertEqual(u'', obj.get_meta_description())
        self.assertEqual(u'', obj.get_meta_keywords())
        obj.meta_title = mtitle
        obj.meta_keywords = mkeys
        obj.meta_description = mdesc
        obj.save()
        self.assertEqual(mtitle, obj.get_page_title())
        self.assertEqual(mkeys, obj.get_meta_keywords())
        self.assertEqual(mdesc, obj.get_meta_description())


class ChainQuerySetTestCase(DjangoTestCase):
    def test_chained_queryset_methods(self):
        title = u'testing_chaining'
        obj = TestModel(title=title)
        obj.save()

        # should be empty because it's not published
        find_published = (TestModel.objects.created_recently()
                          .published().values_list('pk', flat=True))
        self.assertEqual([], list(find_published))

        # should find something unpublished.
        find_unpublished = (TestModel.objects.created_recently()
                            .unpublished().values_list('pk', flat=True))
        self.assertEqual([obj.pk], list(find_unpublished))

        obj.created = datetime.now() - timedelta(days=1)
        obj.is_published = True
        obj.save()
        # still should be empty, because of the created_recently call
        find_published = (TestModel.objects.created_recently()
                          .published().values_list('pk', flat=True))
        self.assertEqual([], list(find_published))

        # still should be empty
        find_unpublished = (TestModel.objects.created_recently()
                            .unpublished().values_list('pk', flat=True))
        self.assertEqual([], list(find_unpublished))

        # should find the thing because it was recently changed by us.
        find_published = (TestModel.objects.modified_recently()
                          .published().values_list('pk', flat=True))
        self.assertEqual([obj.pk], list(find_published))



class SettingsTestCase(UnitTestCase):
    def test_for_values(self):
        self.assertEqual(RECENTLY_MINUTES, 30)
        self.assertEqual(MAX_NUM_RELATIONS, 3)


class ViewOnSiteTestCase(DjangoTestCase):
    def test_calling(self):
        obj = TestModel(title=u'view_on_site_obj')
        obj.save()
        view_on_site = ViewOnSite()
        self.assertIsNotNone(view_on_site(obj))


class SparklineTestCase(DjangoTestCase):
    def test_calling(self):
        obj = TestModel(title=u'view_on_site_obj')
        obj.save()
        ct = ContentType.objects.get_for_model(obj)
        user = User.objects.create(username=str(uuid4()))
        for day_distance in range(0, 10):
            LogEntry.objects.create(content_type=ct, object_id=obj.pk,
                                    user=user, action_flag=2)
        spark = LogEntrySparkline()
        self.assertEqual(2377, len(spark(obj).strip()))

    def test_calling_empty(self):
        obj = TestModel(title=u'view_on_site_obj')
        obj.save()
        spark = LogEntrySparkline()
        result_empty = spark(obj).strip()
        self.assertEqual(10, len(result_empty))
        self.assertEqual(logentry_empty, result_empty)


class RelationCountTestCase(DjangoTestCase):
    def test_calling(self):
        user = User.objects.create(username=str(uuid4()))
        for x in range(1, 4):
            g = Group.objects.create(name=str(x))
            user.groups.add(g)
        counter = RelationCount(accessor='groups', label='test')
        result = counter(user)
        # after calling, we have secretly got these variables.
        self.assertEqual(counter._relcount, 3)
        self.assertEqual(force_unicode(counter._vname[0]), u'user')


class RelationListTestCase(DjangoTestCase):
    def test_calling(self):
        admin.site.register(User)
        admin.site.register(Group)
        user = User.objects.create(username=str(uuid4()))
        for x in range(1, 4):
            g = Group.objects.create(name=str(x))
            user.groups.add(g)
        items = RelationList(accessor='groups', label='test')
        result = items(user)
        self.assertEqual(len(force_unicode(result)), 202)
        self.assertEqual(items._count, 3)

    def test_calling(self):
        admin.site.register(User)
        admin.site.register(Group)
        user = User.objects.create(username=str(uuid4()))
        for x in range(1, 12):
            g = Group.objects.create(name=str(x))
            user.groups.add(g)
        items = RelationList(accessor='groups', label='test', max_num=3)
        result = items(user)
        self.assertEqual(len(force_unicode(result)), 319)
        self.assertEqual(items._count, 11)


class FieldsetsTestCase(UnitTestCase):
    def test_construction(self):
        fieldsets = [
            changetracking_fieldset,
            titles_fieldset,
            publishing_fieldset,
            date_publishing_fieldset,
            seo_fieldset,
        ]
        expecting = ['created', 'modified', 'title', 'menu_title',
                     'is_published', 'publish_on', 'unpublish_on',
                     'meta_title', 'meta_description', 'meta_keywords']
        fields = flatten_fieldsets(fieldsets)
        self.assertEqual(fields, expecting)
