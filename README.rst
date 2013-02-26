About django-helpfulfields
==========================

:author: Keryn Knight

Mostly a collection of `Django`_ models, querysets, and admin stuff. Because
I'm tired of copy-pasting and tweaking the same bits over and over between
projects, so I'm trying to package up the pieces into a bunch of
reusable quasi-components, importable into any `Django`_ project.

Documentation
-------------

Documentation is available via the wonderful `Read the docs`_ - the
`latest build`_ can be found at https://django-helpfulfields.readthedocs.org/en/latest/index.html.

Things it provides
------------------

Currently, the following things are provided:

 * Models for:

   * created & modified fields.
   * title & menu title fields.
   * meta title, description and keywords fields.
   * a published boolean field.
   * published date-range fields.
   * pre-set generic foreign key fields.
   * a soft delete field.

 * Querysets for:

   * all the model variants listed above.

 * Admin helpers for:

   * a link on each changelist object to "view on site"
   * a count of related items for an object in the changelist.
   * a list of related items for an object in the changelist.
   * a sparkline of change frequency for an object in the changelist.

 * A whole bunch of strings marked for translation.

Contributing
------------

There is a `GitHub`_ repository at `kezabelle/django-helpfulfields`_ which
is the canonical location for involvement. Use the app. Open issues. Tell me
how it could suck less.

Bug reports and feature requests can be filed on the repository's `issue tracker`_.

If something can be discussed in 140 character chunks, there's also `my Twitter account`_.

License
-------

It's `FreeBSD`_. a ``LICENSE`` file can be found in the root of the repository,
and should also be present in any distributed downloads.


Status
------

`unit tests`_ are now available, via ``python setup.py test`` or
``python manage.py test helpfulfields``, which should be slightly re-assuring;
there are currently **12** test cases, split into **19** individual tests, which
assert **61** variants.

Below is the coverage report from ``python setup.py test``, for the
current version::

    Name                      Stmts   Miss  Cover   Missing
    -------------------------------------------------------
    helpfulfields/admin         113      9    92%   161, 285, 297-307, 314-320
    helpfulfields/models         94      8    91%   282-287, 298-305
    helpfulfields/querysets      39      6    85%   156-157, 167-168, 177-178
    helpfulfields/settings        2      0   100%
    helpfulfields/text           37      1    97%   9
    -------------------------------------------------------
    TOTAL                       285     24    92%

.. _Django: https://www.djangoproject.com/
.. _Read the docs: https://readthedocs.org/
.. _latest build: https://django-helpfulfields.readthedocs.org/en/latest/index.html
.. _GitHub: https://github.com/
.. _kezabelle/django-helpfulfields: https://github.com/kezabelle/django-helpfulfields/tree/master
.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
.. _issue tracker: https://github.com/kezabelle/django-helpfulfields/issues/
.. _my Twitter account: https://twitter.com/kezabelle/
.. _unit tests: https://docs.djangoproject.com/en/stable/topics/testing/
