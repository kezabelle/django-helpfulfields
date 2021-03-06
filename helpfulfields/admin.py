# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging
from operator import itemgetter
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import Template, Context
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.translation import string_concat
from helpfulfields.settings import MAX_NUM_RELATIONS
from helpfulfields.text import (seo_fieldset_label, changetracking_fieldset_label,
                                dates_fieldset_label, view_on_site_label,
                                object_not_mounted, logentry_label,
                                logentry_empty)

logger = logging.getLogger(__name__)

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
    An object capable of being used in the
    :class:`~django.contrib.admin.ModelAdmin`
    :attr:`~django.contrib.admin.ModelAdmin.list_display` to enable a link to
    the current object on the frontend of the website::

        class MyModelAdmin(ModelAdmin):
            list_display = ['pk', ViewOnSite('column name', 'view on site!')]

    which shows a link to view an object on the live site, assuming the `obj`
    has :meth:`~django.db.models.Model.get_absolute_url` defined.

    :test case: :class:`helpfulfields.tests.ViewOnSiteTestCase`
    """
    def __init__(self, text=view_on_site_label, label=view_on_site_label):
        """
        :param text: The text to display for each item, eg: "View on site"
        :param label: the short description for the
                      :meth:`~django.contrib.admin.ModelAdmin.changelist_view`
                      changelist column.
        """
        self.short_description = label
        self.__name__ = label
        self.text = text
        self.allow_tags = True

    def __call__(self, obj):
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
            u'content_type': ContentType.objects.get_for_model(obj).pk,
            u'pk': obj.pk,
            u'text': escape(force_unicode(self.text))
        }


class RelationCount(object):
    """
    An object capable of being used in the
    :class:`~django.contrib.admin.ModelAdmin`
    :attr:`~django.contrib.admin.ModelAdmin.list_display` to enable a count of
    related items::

        class MyModelAdmin(ModelAdmin):
            list_display = ['pk', RelationCount('relation_name', 'item count')]

    which adds a new column to the admin which shows the results of
    ``obj.accessor.count()`` and the verbose name.

    .. note::
        We expect to be able to address the relation from the ``obj`` instance.
        As such, reverse relations denied via setting a ``related_name`` of ``+``
        won't work.

    .. warning::
        This should result in a maximum of **one** additional query being
        executed, *per object, per usage*, to get a count of related objects.

    :test case: :class:`helpfulfields.tests.RelationCountTestCase`
    """
    def __init__(self, accessor, label):
        """
        :param accessor: The attribute to look for on each ``obj`` (Model instance)
        :param label: the short description for the
                      :meth:`~django.contrib.admin.ModelAdmin.changelist_view`
                      changelist column.
        """
        self.accessor = accessor
        self.short_description = label
        self.__name__ = label

    def __call__(self, obj):
        """
        adds a new column to the admin which shows the results of
        ``obj.accessor.count()`` and the verbose name.

        .. note::
            Doesn't currently handle pluralisation properly.

        :param obj: the current object in the changelist loop.
        :return: a count and verbose name, eg: *3 categories*.
        :rtype: unicode string.
        """
        relation = getattr(obj, self.accessor)
        self._relcount = relation.count()
        self._vname = obj._meta.get_field_by_name(self.accessor)[0].opts.verbose_name,
        return u'%(count)d %(verbose_name)s' % {
            'count': self._relcount,
            'verbose_name': self._vname,
        }


class RelationList(object):
    """
    An object capable of being used in the
    :class:`~django.contrib.admin.ModelAdmin`
    :attr:`~django.contrib.admin.ModelAdmin.list_display` to show a linked list
    of related items::

        class MyModelAdmin(ModelAdmin):
            list_display = ['pk', RelationList('accessor', 'item count')]

    which adds a new column to the admin which shows the results of
    ``obj.accessor.all()`` as links to the appropriate modeladmin page.

    .. note::
        We expect to be able to address the relation from the ``obj`` instance.
        As such, reverse relations denied via setting a ``related_name`` of ``+``
        won't work.

    .. warning::
        It is worth highlighting that this should result in a maximum
        of **one** additional query being executed, *per object, per usage*, to
        get list of related objects. Changing the
        :class:`~django.contrib.admin.ModelAdmin` to use
        :meth:`~django.db.models.query.QuerySet.select_related` and/or
        :meth:`~django.db.models.query.QuerySet.prefetch_related` may remove
        this extra query.

    :test case: :class:`helpfulfields.tests.RelationListTestCase`
    """
    def __init__(self, accessor, label, max_num=MAX_NUM_RELATIONS,
                 more_separator=None, admin_site='admin'):
        """
        :param accessor: The attribute to look for on each ``obj``
                              (Model instance)
        :param label: the short description for the
                      :meth:`~django.contrib.admin.ModelAdmin.changelist_view`
                      changelist column.
        :param max_num: The maximum number of related item links to show.
        :param more_separator: the content between items, and the "N more" link.
        :param admin_site: the URL namespace of the admin.
        """
        self.accessor = accessor
        self.max_num = max_num
        self.short_description = label
        self.__name__ = label
        self.admin_url = admin_site
        self.more_content = more_separator or u'&hellip;'
        self.allow_tags = True

    def __call__(self, obj):
        """
        adds a new column to the admin which shows the results of
        ``obj.accessor.all()`` as links to the appropriate modeladmin page.

        :param obj: the current object in the changelist loop.
        :return: a comma separated list of links to the related objects.
        :rtype: unicode string.
        """
        relation = getattr(obj, self.accessor)
        if callable(relation):
            relation = relation()
        # TODO: it'd be really nice if this could handle methods on ``obj``
        relation_obj = obj._meta.get_field_by_name(self.accessor)[0]
        url_parts = {
            'admin': self.admin_url,
            'module': relation_obj.opts.app_label,
            'klass': relation_obj.opts.module_name,
        }
        cl_link = '%(admin)s:%(module)s_%(klass)s_changelist'
        c_link = '%(admin)s:%(module)s_%(klass)s_change'
        try:
            url = reverse(cl_link % url_parts)
        except NoReverseMatch:
            # Unable to find the relation mounted on the admin, we may throw
            # the problem up to the user if in debug mode, otherwise we log it
            # and move on.
            if settings.DEBUG:
                raise
            logger.debug(object_not_mounted % {
                'verbose_name': relation_obj.opts.object_name,
                'site': u'"%s"' % self.admin_url,
            })
            return u''

        # force evaluation now, so that we know what we've got in 1 query.
        # We need the whole list, even if we're discarding some of it, so that
        # we know what primary keys to filter the "more" changelist link for.
        try:
            object_list = list(relation.all())
        except AttributeError:
            # If for some reason it's not a descriptor/manager for a relation
            # queryset - perhaps it's a foreign key or something. We'll hope
            # for the best that we can continue.
            # If relation is None, (a null FK, for example), continue assuming
            # there's no relations to deal with.
            object_list = list([relation])

        n_more = u'%(url)s?id__in=%(filter_pks)s' % {
            'url': url,
            'filter_pks': ','.join([force_unicode(x.pk) for x in object_list]),
        }
        self._count = len(object_list)

        # handle adding the "... 3 more" to the content.
        more_link = u''
        if self._count > self.max_num:
            more_parts = {
                'url': n_more,
                'count': self._count - self.max_num,
                'separator': self.more_content,
            }
            more_link = (u'%(separator)s<a href="%(url)s" '
                         u'class="changelist-morerelatedlink">%(count)d'
                         u'&nbsp;more</a>' % more_parts)

        # handle generating the admin edit link for each individual relation.
        edit_link = (u'<a href="%(url)s" class="changelist-relatedlink"'
                     u'>%(link)s</a>')
        items = u', '.join([
            edit_link % {
                'url': reverse(c_link % url_parts, args=(x.pk,)),
                'link': escape(x)
            }
            for x in object_list[0:self.max_num]
        ])

        # more_link may be empty ...
        return string_concat(items, more_link)


class LogEntrySparkline(object):
    """
    An object capable of being used in the
    :class:`~django.contrib.admin.ModelAdmin`
    :attr:`~django.contrib.admin.ModelAdmin.list_display` to show a tiny
    HTML-only sparkline of recent changes made via the admin::

        class MyModelAdmin(ModelAdmin):
            list_display = ['pk', LogEntrySparkline(days=60)]

    .. warning::
        It is worth highlighting that this will potentially result in a maximum
        of **two** additional queries being executed, *per object*, to get
        the :class:`~django.contrib.contenttypes.models.ContentType` and the
        :class:`~django.contrib.admin.models.LogEntry` items.

        This will be amortized down to **one** query, once all needed
        :class:`~django.contrib.contenttypes.models.ContentType` objects have
        been cached internally by `Django`_.

    .. note::
        For the sake of being portable, and not requiring we be in the
        `INSTALLED_APPS`, the HTML and CSS are actually declared
        on this class, rather than via a template which we might
        :func:`~django.template.loader.render_to_string`. This may yet be a
        mistake, so the API methods should be considered private.

    An example of the output is provided below, though it may render slightly
    differently due to font-sizing differences between this documentation and
    the standard `Django`_ :class:`~django.contrib.admin.AdminSite`:

    .. raw:: html

        <div class="changelist-sparkline" style="overflow:hidden;border-bottom:1px dotted #5b80b2;height:1em; display:inline-block;">
            <div class="changelist-sparkline-bar" style="height:0.3em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.5em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.6em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:1em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:1em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.8em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.1em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.2em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.35em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.6em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.75em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:1em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
            <div class="changelist-sparkline-bar" style="height:0.3em;width:0.3em;vertical-align:baseline;margin:0 0.05em;display:inline-block;background-color:#7CA0C7;"></div>
        </div>

    :test case: :class:`helpfulfields.tests.SparklineTestCase`
    """
    def __init__(self, days=14, label=logentry_label):
        """
        :param days: How far back should we generate a sparkline for.
        :param label: the short description for the
                      :meth:`~django.contrib.admin.ModelAdmin.changelist_view`
                      changelist column.
        """
        self.short_description = label
        self.__name__ = label
        self.days = days
        self.allow_tags = True

    def __call__(self, obj):
        """
        generates the necessary data for displaying a sparkline.

        :param obj: the current object in the changelist loop.
        :return: the HTML representing the sparkline graph.
        :rtype: unicode string.
        """
        ct = ContentType.objects.get_for_model(obj)
        now = datetime.now()
        back_to = now - timedelta(days=self.days)

        # get all entries for this object in the last N days.
        # Note: It doesn't matter what order results are returned in, as
        # we're popping them into a separate, unsorted data structure anyway.
        entries = LogEntry.objects.filter(content_type=ct, object_id=obj.pk,
                                          action_time__gte=back_to)

        # generate the initial list of items.
        days_with_counts = {}
        for day_distance in range(0, self.days):
            new_datetime = now - timedelta(days=day_distance)
            days_with_counts[new_datetime.date()] = 0

        # populate the existing dates with change counts.
        for entry in entries:
            days_with_counts[entry.action_time.date()] += 1

        maximum = max(days_with_counts.values()) #: 1em / 100%
        if maximum < 1:
            return logentry_empty

        days_with_css_vals = {}
        for key, val in days_with_counts.items():
            val_as_percentage = val / maximum
            days_with_css_vals[key] = val_as_percentage

        results = sorted(days_with_css_vals.items(), key=itemgetter(0))

        ctx = Context({
            'sparks': results,
            'sparkbar_css': self._sparkline_bar_css(),
            'sparkline_css': self._sparkline_graph_css()
        })
        return self._sparkline_template().render(ctx)

    def _sparkline_bar_css(self):
        """
        generates the necessary CSS for an individual bar on the graph.

        :return: the CSS, as minified as we can get it.
        :rtype: unicode string.
        """
        css = {
            'width': '0.3em',
            'margin': '0 0.05em',
            'display': 'inline-block',
            'background-color': '#7CA0C7',
            'vertical-align': 'baseline',
        }
        return ''.join(['%s:%s;' % rule_val for rule_val in css.items()])

    def _sparkline_graph_css(self):
        """
        generates the necessary CSS for the sparkline graph itself.

        :return: the CSS, as minified as we can get it.
        :rtype: unicode string.
        """
        css = {
            'height': '1em',
            'border-bottom': '1px dotted #5b80b2',
            'overflow': 'hidden',
        }
        return ''.join(['%s:%s;' % rule_val for rule_val in css.items()])

    def _sparkline_template(self):
        """
        generates the HTML, implements each bar and the appropriate CSS.

        :return: the template, ready to be rendered.
        :rtype: :class:`~django.template.base.Template`
        """
        return Template('''{% spaceless %}
        <div class="changelist-sparkline" style="{{ sparkline_css }}">
        {% for date, spark in sparks %}
            <div class="changelist-sparkline-bar" style="height:{{ spark }}em;{{ sparkbar_css }}"></div>
        {% endfor %}
        </div>
        {% endspaceless %}''')
