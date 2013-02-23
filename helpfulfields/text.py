# -*- coding: utf-8 -*-
import os
from django.utils.translation import ugettext_lazy as _

# This horridness is required so that when we build the documentation, strings
# are evaluated immeidiately, so that we don't have things like
# <django.utils.functional.__proxy__ object at 0x...> everywhere.
if os.environ.get('READTHEDOCS', None) == 'True':
    from django.utils.translation import ugettext as _

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.Titles.title` field on
#: :class:`~helpfulfields.models.Titles`
titles_title_label = _(u'title')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.Titles.menu_title` field on
#: :class:`~helpfulfields.models.Titles`
titles_menu_label = _(u'menu title')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.Titles.menu_title` field on
#: :class:`~helpfulfields.models.Titles`
titles_menu_help = _(u'may be displayed in menus, instead of the standard title')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.SEO.meta_title` field on
#: :class:`~helpfulfields.models.SEO`
seo_title_label = _(u'page title')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.SEO.meta_title` field on
#: :class:`~helpfulfields.models.SEO`
seo_title_help = _(u'displayed by the web browser in the window/tab/taskbar.')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.SEO.meta_description` field on
#: :class:`~helpfulfields.models.SEO`
seo_description_label = _(u'page description')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.SEO.meta_description` field on
#: :class:`~helpfulfields.models.SEO`
seo_description_help = _(u'may be displayed by search engines in results.')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.SEO.meta_keywords` field on
#: :class:`~helpfulfields.models.SEO`
seo_keywords_label = _(u'page keywords')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.SEO.meta_keywords` field on
#: :class:`~helpfulfields.models.SEO`
seo_keywords_help = _(u'may be used by search engines to flag you as spamming.')

#: the name for the fieldset provided in
#: :mod:`~helpfulfields.admin.seo_fieldset`
seo_fieldset_label = _(u'search engine optimisation')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.SoftDelete.deleted`
#: field on :class:`~helpfulfields.models.SoftDelete`
soft_delete_label = _(u'deleted?')

#: the `help_text` for the :attr:`~helpfulfields.models.SoftDelete.deleted`
#: field on :class:`~helpfulfields.models.SoftDelete`
soft_delete_help = _(u'has this been removed from the website?')

#: the initial state text for the
#: :attr:`~helpfulfields.models.SoftDelete.DELETED_CHOICES` on
#: :class:`~helpfulfields.models.SoftDelete`
soft_delete_initial = _(u'unmodified')

#: the state text for restored items on the
#: :attr:`~helpfulfields.models.SoftDelete.DELETED_CHOICES` on
#: :class:`~helpfulfields.models.SoftDelete`
soft_delete_false = _(u'restored')

#: the state text for deleted items on the
#: :attr:`~helpfulfields.models.SoftDelete.DELETED_CHOICES` on
#: :class:`~helpfulfields.models.SoftDelete`
soft_delete_true = _(u'deleted')

#: the name for the fieldset provided in
#: :mod:`~helpfulfields.admin.changetracking_fieldset`
changetracking_fieldset_label = _(u'changes')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.ChangeTracking.created` field on
#: :class:`~helpfulfields.models.ChangeTracking`
created_label = _(u'created')

#: the `help_text` for the :attr:`~helpfulfields.models.ChangeTracking.created`
#: field on :class:`~helpfulfields.models.ChangeTracking`
created_help = _(u'the date and time on which this object was first added')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.ChangeTracking.modified` field on
#: :class:`~helpfulfields.models.ChangeTracking`
modified_label = _(u'last modified')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.ChangeTracking.modified` field on
#: :class:`~helpfulfields.models.ChangeTracking`
modified_help = _(u'the date and time on which this object was last changed')

#: the name for the fieldset provided in
#: :mod:`~helpfulfields.admin.date_publishing_fieldset`
dates_fieldset_label = _(u'publishing info')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.Publishing.is_published` field on
#: :class:`~helpfulfields.models.Publishing`
quick_publish_label = _(u'is published')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.Publishing.is_published` field on
#: :class:`~helpfulfields.models.Publishing`
quick_publish_help = _(u'should this object be visible on the website')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.DatePublishing.publish_on` field on
#: :class:`~helpfulfields.models.DatePublishing`
publish_label = _(u'publishing date')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.DatePublishing.publish_on` field on
#: :class:`~helpfulfields.models.DatePublishing`
publish_help = _(u'the date and time on which this object should be visible on '
                 u'the website.')

#: :attr:`~django.db.models.Field.verbose_name`/:attr:`~django.forms.Field.label`
#: for the :attr:`~helpfulfields.models.DatePublishing.unpublish_on` field on
#: :class:`~helpfulfields.models.DatePublishing`
unpublish_label = _(u'publishing end date')

#: the `help_text` for the
#: :attr:`~helpfulfields.models.DatePublishing.unpublish_on` field on
#: :class:`~helpfulfields.models.DatePublishing`
unpublish_help = _(u'if filled in, this date and time are when this object '
                   u'will cease being available.')

#: text for an exception used by :class:`~helpfulfields.models.SoftDelete` when
#: trying to delete an unsaved object.
object_lacks_pk = _(u"%(model)s object can't be deleted because its %(pk)s "
                    u"attribute is set to None.")

#: text for an exception used by :class:`~helpfulfields.models.SoftDelete` when
#: trying to restore an object which hasn't been deleted.
object_not_deleted = _(u"%(model)s object can't be restored because it has not "
                       u"been deleted.")

#: text used by :class:`~helpfulfields.admin.ViewOnSite` to display in a
#: :class:`~django.contrib.admin.ModelAdmin`'s `list_display`
view_on_site_label = _(u'view on site')

#: text used by :class:`~helpfulfields.admin.RelationList` to log a
#: :exc:`~django.core.urlresolvers.NoReverseMatch`
object_not_mounted = _(u'the %(verbose_name)s is not mounted on admin site %(site)s.')

#: text used by :class:`~helpfulfields.admin.LogEntrySparklines` for displaying
#: a default value in the changelist column header.
logentry_label = _(u'change history')

#: text used by :class:`~helpfulfields.admin.LogEntrySparklines` for scenarios
#: in which there are no :class:`~django.contrib.admin.models.LogEntry`
#: objects for the given period.
logentry_empty = _(u'no changes')
