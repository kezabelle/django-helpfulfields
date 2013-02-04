# -*- coding: utf-8 -*-
# All the text strings we need to mark for translation go in here.
# By putting them here, we can keep everything nice and tidy, and, bonus, we don't
# have to jump through long-winded hoops to get the verbose_name from a Model
# to be the label for an overridden Form field.
from django.utils.translation import ugettext_lazy as _

titles_title_label = _(u'title')
titles_menu_label = _(u'menu title')
titles_menu_help = _(u'may be displayed in menus, instead of the standard title')

seo_title_label = _(u'page title')
seo_title_help = _(u'displayed by the web browser in the window/tab/taskbar.')
seo_description_label = _(u'page description')
seo_description_help = _(u'may be displayed by search engines in results.')
seo_keywords_label = _(u'page keywords')
seo_keywords_help = _(u'may be used by search engines to flag you as spamming.')

seo_fieldset_label = _(u'search engine optimisation')

soft_delete_label = _(u'deleted?')
soft_delete_help = _(u'has this been removed from the website?')

soft_delete_initial = _(u'unmodified')
soft_delete_false = _(u'restored')
soft_delete_true = _(u'deleted')

changetracking_fieldset_label = _(u'changes')

dates_fieldset_label = _(u'publishing info')

publish_label = _(u'publishing date')
publish_help = _(u'the date and time on which this object should be visible on '
    u'the website.')
unpublish_label = _(u'publishing end date')
unpublish_help = _(u'if filled in, this date and time are when this object will '
    u'cease being available.')

view_on_site_label = _(u'View on site')
