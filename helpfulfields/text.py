# -*- coding: utf-8 -*-
# All the text strings we need to mark for translation go in here.
# By putting them here, we can keep everything nice and tidy, and, bonus, we don't
# have to jump through long-winded hoops to get the verbose_name from a Model
# to be the label for an overridden Form field.
from django.utils.translation import ugettext_lazy as _

titles_title_label = _(u'title')
titles_menu_label = _(u'menu title')
titles_menu_help = _(u'may be displayed in menus, instead of the standard title')
publish_label = _(u'publishing date')
publish_help = _(u'the date and time on which this object should be visible on '
    u'the website.')
unpublish_label = _(u'publishing end date')
unpublish_help = _(u'if filled in, this date and time are when this object will '
    u'cease being available.')
