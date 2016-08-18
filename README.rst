The goal of ``plone.app.widgets`` is to provide an implementation for a new set
of javascript widgets being developed outside Plone as part of `Mockup`_
project. It overrides explicit widgets used in dexterity and archetypes to
provide tested and modularized widgets based on the concept of *patterns*.

.. image:: https://travis-ci.org/plone/plone.app.widgets.png?branch=master
    :alt: Travis CI badge
    :target: https://travis-ci.org/plone/plone.app.widgets

.. image:: https://coveralls.io/repos/plone/plone.app.widgets/badge.png?branch=master
    :alt: Coveralls badge
    :target: https://coveralls.io/r/plone/plone.app.widgets?branch=master

.. image:: https://pypip.in/v/plone.app.widgets/badge.png
    :target: https://crate.io/packages/plone.app.widgets

.. image:: https://pypip.in/d/plone.app.widgets/badge.png
    :target: https://crate.io/packages/plone.app.widgets

.. image:: https://saucelabs.com/browser-matrix/plone-pa-widgets.svg
    :target: https://saucelabs.com/u/plone-pa-widgets


.. contents::


1.x
===

The 1.x branch of plone.app.widgets is to be used only for Plone 4.3. 2.x
is only to be used with Plone 5.


Is safe to use this package?
============================

This package should be safe to install and easy to uninstall (there is also
uninstall profile). That means its fairly safe to give it a try, but just in
case don't forget to create backup before testing it.


What is included?
=================

The fields that are using updated widgets are:

- **Tags field** (AjaxSelectWidget)
- **Language field** (SelectWidget)
- **Effective date field** (DatetimeWidget)
- **Expire date field** (DatetimeWidget)
- **Contributors field** (AjaxSelectWidget)
- **Creators field** (AjaxSelectWidget)
- **Related items field** (RelatedItemsWidget)
- **Query string field** (QueryStringWidget) in case `plone.app.contenttypes`_
  is installed.
- **Text field** (TinyMCEWidget) for ATContentTypes 'text' field, and for
  use in `plone.app.contenttypes` (optional).  This may be used for other
  content types in add-ons, but may require additional configuration and/or
  registration for broader use when `plone.app.contenttypes` is not installed
  in a Plone 4 site.

All client side code (javascript/css/images) is done and tested as part of
`Mockup`_ project.

.. image:: https://travis-ci.org/plone/mockup.png
   :target: https://travis-ci.org/plone/mockup
   :alt: Travis CI

.. image:: https://coveralls.io/repos/plone/mockup/badge.png?branch=master
   :target: https://coveralls.io/r/plone/mockup?branch=master
   :alt: Coveralls

.. image:: https://d2weczhvl823v0.cloudfront.net/plone/mockup/trend.png
   :target: https://bitdeli.com/free
   :alt: Bitdeli

For any feature / bug / comment please create an issue in the `issue tracker`_.


Installation
============

For now only tested with latest Plone 4.3::

    [buildout]
    extends =
        http://dist.plone.org/release/4.3-latest/versions.cfg
        https://raw.github.com/plone/plone.app.widgets/master/versions.cfg
    versions = versions
    parts = instance

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    eggs =
        Pillow
        Plone
        plone.app.widgets[archetypes,dexterity]
    zcml =
        plone.app.widgets

Make sure you install the "Plone Widgets" profile when creating your Plone site
or include ``plone.app.widgets:default`` profile in your ``metadata.xml``..


.. _`Mockup`: http://plone.github.io/mockup
.. _`issue tracker`: https://github.com/plone/mockup/issues?labels=widgets
.. _`PLIP here`: https://dev.plone.org/ticket/13476
.. _`plone.app.toolbar`: https://github.com/plone/plone.app.toolbar
.. _`plone.app.contenttypes`: https://github.com/plone/plone.app.contenttypes
