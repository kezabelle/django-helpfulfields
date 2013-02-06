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
        return 1
    view_on_site.allow_tags = True
    view_on_site.short_description = view_on_site_label
