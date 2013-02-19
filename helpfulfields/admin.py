# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from helpfulfields.text import (seo_fieldset_label, changetracking_fieldset_label,
                                dates_fieldset_label, view_on_site_label)

#: a fieldset for use in a :class:`~django.contrib.admin.ModelAdmin`
#: :attr:`~django.contrib.admin.ModelAdmin.fieldsets` definition
#: to display objects which are making use of the
#: :attr:`~helpfulfields.models.Titles.title` and
#: :attr:`~helpfulfields.models.Titles.menu_title` provided by
#: :class:`~helpfulfields.models.Titles`.
#: This fieldset does not provide a name, as the field names should be self
#: descriptive at a very basic level.
titles_fieldset = [
    None, {
        'classes': [],
        'fields': [
            'title',
            'menu_title',
        ]
    }
]

#: a fieldset for use in a :class:`~django.contrib.admin.ModelAdmin`
#: :attr:`~django.contrib.admin.ModelAdmin.fieldsets` definition
#: to display objects which are making use of the
#: :attr:`~helpfulfields.models.Publishing.is_published` field provided by
#: :class:`~helpfulfields.models.Publishing`.
#: This fieldset does not provide a name, because it doesn't make much sense
#: for one field.
publishing_fieldset = [
    None, {
        'classes': [],
        'fields': [
            'is_published',
        ]
    }
]

#: a fieldset for use in a :class:`~django.contrib.admin.ModelAdmin`
#: :attr:`~django.contrib.admin.ModelAdmin.fieldsets` definition
#: to display objects which are making use of the
#: :attr:`~helpfulfields.models.DatePublishing.publish_on` and
#: :attr:`~helpfulfields.models.DatePublishing.unpublish_on` provided by
#: :class:`~helpfulfields.models.DatePublishing`.
#: The fieldset provides a translated name via
#: :attr:`~helpfulfields.text.dates_fieldset_label`
date_publishing_fieldset = [
    dates_fieldset_label, {
        'classes': [],
        'fields': [
            'publish_on',
            'unpublish_on',
        ]
    }
]

#: a fieldset for use in a :class:`~django.contrib.admin.ModelAdmin`
#: :attr:`~django.contrib.admin.ModelAdmin.fieldsets` definition
#: to display objects which are making use of the
#: :attr:`~helpfulfields.models.SEO.meta_title`,
#: :attr:`~helpfulfields.models.SEO.meta_description` and
#: :attr:`~helpfulfields.models.SEO.meta_keywords` provided by
#: :class:`~helpfulfields.models.SEO`.
#: The fieldset provides a translated name via
#: :attr:`~helpfulfields.text.seo_fieldset_label`, and collapses itself by
#: default.
seo_fieldset = [
    seo_fieldset_label, {
        'classes': [
            'collapse'
        ],
        'fields': [
            'meta_title',
            'meta_description',
            'meta_keywords',
        ]
    }
]

#: a list for use in a :class:`~django.contrib.admin.ModelAdmin`'s
#: :attr:`~django.contrib.admin.ModelAdmin.readonly_fields` configuration
#: to avoid allowing editing of the
#: :attr:`~helpfulfields.models.ChangeTracking.created` and
#: :attr:`~helpfulfields.models.ChangeTracking.modified` fields provided by
#: :class:`~helpfulfields.models.ChangeTracking`
changetracking_readonlys = ['created', 'modified']

#: a fieldset for use in a :class:`~django.contrib.admin.ModelAdmin`
#: :attr:`~django.contrib.admin.ModelAdmin.fieldsets` definition
#: to display objects which are making use of the
#: :attr:`~helpfulfields.models.ChangeTracking.created` and
#: :attr:`~helpfulfields.models.ChangeTracking.modified` fields provided by
#: :class:`~helpfulfields.models.ChangeTracking`.
#: The fieldset provides a translated name via
#: :attr:`~helpfulfields.text.changetracking_fieldset_label`, and starts out
#: collapsed as the data is unimportant.
changetracking_fieldset = [
    changetracking_fieldset_label, {
        'classes': [
            'collapse'
        ],
        'fields': [
            'created',
            'modified',
        ]
    }
]


class ViewOnSite(object):
    """
    An object capable of being mixed into a standard
    :class:`~django.contrib.admin.ModelAdmin` to enable use in the
    :attr:`~django.contrib.admin.ModelAdmin.list_display`::

        class MyModelAdmin(ViewOnSite, ModelAdmin):
            list_display = ['__unicode__', 'view_on_site']

    which shows a link to view an object on the live site, assuming the `obj`
    has :meth:`~django.db.models.Model.get_absolute_url` defined.
    """
    def view_on_site(self, obj):
        """
        link to view an object on the live site, assuming the `obj`
        has :meth:`~django.db.models.Model.get_absolute_url` defined.

        :param obj: the current object in the changelist loop.
        :return: a link for viewing on the site.
        :rtype: unicode string.
        """
        if not hasattr(obj, 'get_absolute_url'):
            return u''

        output = (u'<a href="../../r/%(content_type)d/%(pk)d/" class="'
                  u'changelist-viewsitelink">%(text)s</a>')
        return output % {
            'content_type': ContentType.objects.get_for_model(obj).pk,
            'pk': obj.pk,
            'text': force_unicode(view_on_site_label)
        }
    view_on_site.allow_tags = True
    view_on_site.short_description = view_on_site_label
