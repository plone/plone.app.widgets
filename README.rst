``plone.app.widgets`` is a revamp of plone widgets. It does this by overriding
the widgets of some of the fields in plone.


.. image:: https://travis-ci.org/plone/plone.app.widgets.png?branch=master


Introduction
============

TODO: explain plone.init.js and how to register a widget


Widgets
=======

List of widgets this package provides.

CalendarWidget
--------------

`pickadate.js`_


AutocompleteWidget
------------------

`textext.js`_


Fields overridden
=================

 - ``effectiveDate`` field with CalendarWidget
 - ``expirationDate`` field with CalendatWidget
 - ``subject`` field with AutocompleteWidget


.. _`pickadate.js`: http://amsul.github.com/pickadate.js
.. _`textext.js`: http://textextjs.com
