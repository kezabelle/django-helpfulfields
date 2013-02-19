# -*- coding: utf-8 -*-
from helpfulfields.text import (seo_fieldset_label, changetracking_fieldset_label,
                                dates_fieldset_label, view_on_site_label)

titles_fieldset = [
    None, {
        'classes': [],
        'fields': [
            'title',
            'menu_title',
        ]
    }
]


publishing_fieldset = [
    None, {
        'classes': [],
        'fields': [
            'is_published',
        ]
    }
]

date_publishing_fieldset = [
    dates_fieldset_label, {
        'classes': [],
        'fields': [
            'publish_on',
            'unpublish_on',
        ]
    }
]

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

changetracking_readonlys = ['created', 'modified']
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

    def view_on_site(self, obj):
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
