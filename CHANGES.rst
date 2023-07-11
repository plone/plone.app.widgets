Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

5.0.0 (2023-07-11)
------------------

Breaking changes:


- Make this package deprecated. Widget base classes moved to ``plone.app.z3cform.widgets.patterns``.
  Also see ``plone.app.widgets.utils`` for information about moving utility methods to their new location.
  [petschki] (#220)


4.0.1 (2023-02-22)
------------------

Bug fixes:


- Depend on plone.base (#222)


4.0.0 (2022-12-05)
------------------

Bug fixes:


- Final release for Plone 6.0.0.
  Note that new code should not use this package, if possible.
  Prefer using code from ``plone.app.z3cform``.
  But some code still needs to be moved there, see `issue 220 <https://github.com/plone/plone.app.widgets/issues/220>`_.
  [maurits] (#600)


4.0.0b1 (2022-08-30)
--------------------

Bug fixes:


- Fix random failing robottests.
  [petschki] (#219)


4.0.0a2 (2022-05-15)
--------------------

Bug fixes:


- add logging in exception handler when loading of tinymce settings is failing [MrTango] (#216)
- Removed z3c.autoinclude.plugin entrypoint. [maurits] (#3188)


4.0.0a1 (2022-04-05)
--------------------

New features:


- PLIP 3211 - Remove implicit dependency on Mockup. (#210)
- Update datetime pattern options for Patternslib pat-date-picker/pat-datetime-picker.
  [petschki] (#213)


Bug fixes:


- fix robot tests
  [petschki] (#214)


3.0.6 (2021-09-15)
------------------

Bug fixes:


- Remove cyclic dependency with plone.app.z3cform
  [sneridagh] (#211)


3.0.5 (2020-10-30)
------------------

Bug fixes:


- Robot tests: Fix deprecated jQuery.size.
  [thet] (#207)


3.0.4 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


3.0.3 (2019-11-25)
------------------

Bug fixes:


- Run robot tests as Member since the widget will move to the logged-in-bundle.
  [agitator] (#201)


3.0.2 (2019-06-27)
------------------

Bug fixes:


- Adapt the tests to the new robotframework syntax [ale-rt] (#199)


3.0.1 (2019-06-19)
------------------

Bug fixes:


- - Use the shared 'Plone test setup' and 'Plone test teardown' keywords in Robot
    tests.
    [Rotonen] (#195)


3.0.0 (2019-05-04)
------------------

Breaking changes:


- Deprecate ``get_ajaxselect_options`` (no longer used).
  ``IWidgetsLayer`` and ``IWidgetsView`` are no longer used, remove them.
  Deprecated ``IFileFactory`` import, use ``zope.filerepresentation`` instead.
  Hard depend on ``plone.app.event``, it is meanwhile a dependenciy of Plone core.
  Move ``IFieldPermissionChecker`` and ``Zope2FileUploadStorable`` to ``plone.app.z3cform`` in order to slowly fade out this package.
  Use util ``first_weekday`` from ``plone.app.event`` and do not duplicate here; deprecated import placed.
  [jensens] (#194)


2.4.1 (2018-12-28)
------------------

Breaking changes:

- Remove five.globalrequest dependency.
  It has been deprecated upstream (Zope 4).
  [gforcada]

New features:

- Add support for rendering <optgroup> elements from
  zope.schema.interfaces.ITreeVocabulary hierarchical terms.
  [rpatterson]

Bug fixes:

- Remove GS profile pointing to non existing directory.
  [jensens]


2.4.0 (2018-11-07)
------------------

New features:

- Port to python 3.
  [davisagli] [pbauer] [gforcada]

Bug fixes:

- Modernize robot keywords that use "Get Element Attribute"
  [ale-rt]

- Do not depend on `Products.ResourceRegistries` in `setup.py`.
  In the code there is anyway no dependency.
  [jensens]


2.3.1 (2018-03-10)
------------------

Bug fixes:

- Minor administrative cleanups.


2.3 (2018-02-05)
----------------

New features:

- Related items widget: show a recently used dropdown, but do not activate it.
  plone.app.relationfield itself is activating the "recently used" feature.
  The "recently used" dropdown is only available for Mockup 2.6.3+.
  [thet]

Bug fixes:

- Add Python 2 / 3 compatibility
  [pbauer]

- Marked unstable robotframework test as noncritical.
  And maybe fix it by using keyword ``Wait Until Page Does Not Contain Element``.
  [maurits]


2.2.2 (2017-09-05)
------------------

New features:

- Pass parameter of subwidgets to the query string widget to get them properly initialized.
  Fixes a problem where the related items widget behaved differently from other areas and the date widget didn't respect the users localization.
  [thet]


2.2.1 (2017-08-27)
------------------

Bug fixes:

- Allow related items options to work on non OFS Simple Item objects.
  [thet]


2.2 (2017-07-03)
----------------

New features:

- Related items widget options changes:
  - Let the browsing/searching start path be the current context if its folderish or a level up.
  - Include the ``contextPath`` option to exclude the current context from selection.
  - Include the ``favorites`` option with the current context and the navigation root to quickly jump to these paths.
  - Clean up obsolete options.
  Fixes https://github.com/plone/Products.CMFPlone/issues/1974
  [thet]

Bug fixes:

- Change deprecated unittest method ``assertEquals`` to ``assertEqual``.
  [thet]


2.1 (2017-02-20)
----------------

Bug fixes:

- Change options ``today`` and ``clear`` to reflect changes in mockup 2.4.
  Refs: PR #154
  [thet]

- Root the related items widget path bar to the top most visible site in the url and not the portal object itself.
  This avoids related item widgets in subsites being able to break out of their virtual hosting root.
  [thet]


2.0.7 (2016-11-19)
------------------

Bug fixes:

- No longer test on Travis.  We are tested on jenkins.plone.org, and
  the Travis setup on master is pretty broken.  [maurits]

- Take more time during robot tests.
  I hope that this makes a sometimes failing test always pass.  [maurits]
- Root the related items widget path bar to the top most visible site in the url and not the portal object itself.
  This avoids related item widgets in subsites being able to break out of their virtual hosting root.
  [thet]

- Root the related items widget path bar to the top most visible site in the url and not the portal object itself.
  This avoids related item widgets in subsites being able to break out of their virtual hosting root.
  [thet]


2.0.6 (2016-08-18)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


2.0.5 (2016-04-28)
------------------

Fixes:

- Fix related items to search for the whole site rather than from the navigation root only.
  [Gagaro]


2.0.4 (2016-02-27)
------------------

New:

- Add navigation root support to related items widget. Fix incorrect options
  merge for TinyMCE widget.
  [alecm]

Fixes:

- Ensure vocabulary lookup works on add forms for related items widget.
  [alecm]

- Ensure we have all content for tree query in relateditems
  [Gagaro]

- Sort relateditems tree by sortable_title.
  [Gagaro]

2.0.3 (2016-02-14)
------------------

Fixes:

- Fixed timing issue in robot tests.  [maurits]

- Use plone i18n domain
  [staeff]


2.0.2 (2015-11-28)
------------------

Fixes:

- Removed code for unused types_link_to_folder_contents.
  [maurits]

- Don't install the plone.app.widgets dummy default profile in tests.
  [thet]

2.0.1 (2015-09-21)
------------------

- Pull types_link_to_folder_contents values from the configuration registry.
  [esteele]


2.0.0 (2015-03-26)
------------------

- Add Plone 5 warning.
  [gforcada]

- Include TinyMCE languages from mockup.
  [petschki]

- Raise minimum ``Products.CMFPlone`` requirement to 4.3.4 to ensure
  compatibility with jQuery 1.9+. jQuery 1.11.1 is included in recent
  ``mockup``.
  [thet]

- Always include CSS and JS SourceMap files. They are only loaded, when the
  browser's developer console is open. Replaces previous behavior, where
  uninified (and broken) resources were loaded when mockup was installed, which
  was also an ugly implicit development mode behavior.
  [thet]

- Use a mimetype selector for richtext areas, if multiple mimetypes are allowed.
  [thet]

- Allow to remove a selected option in the ``select2`` widget if the field
  is not required
  [frapell]

- Test fixes.
  [thet]

- add jsi18n integration
  [vangheem, kiorky]


1.7.0 (2014-07-15)
------------------

- Remove configuration of plone.app.event's ``start`` and ``end`` fields in the
  ``dx_bbb`` module. Requires ``plone.app.event >= 1.2``, which does the widget
  configuration by itself. There is no point in using a previous version of
  plone.app.event together with plone.app.widgets.
  [thet]

- Store RelatedItems in correct order.
  [garbas]

1.6.0 (2014-04-20)
------------------

- Add default_timezone widget attribute to the Dexterity DatetimeWidget. If
  used and set to a valid Olson DB/pytz timezone identifier or to an callback
  returning such, the datetime object returned by the widget will be localized
  to that timezone.  This changes the timezone related behavior from version
  1.4.0.
  [thet]

- fix related items widget using getSource when it should use getVocabulary
  [davisagli]


1.5.0 (2014-03-05)
------------------

- robot tests for SelectWidget
  [gforcada]

- make tests pass for plone 5
  [davisagli]

- add more tests for richtext widget
  [amleczko]

- fix querystring converter with empty input
  [davisagli]

- add richtext widget support and remove Products.TinyMCE dependency
  [amleczko]

- Add sphinx-based documentation.
  [tisto]

- move the AT macros to a browser view
  [davisagli]

- make the profile not do anything on plone 5, which already includes the
  widgets bundle in the plone bundle
  [davisagli]

- Fix tests when portal_tinymce is missing.
  [jaroel]

- Create robot tests for querystring widget
  [ale-rt]

- Add DX tinymce test
  [jaroel]

- Fix to import ROBOT_TEST_LEVEL from plone.app.testing.interfaces
  [datakurre]

- RelatedItems widget: use a single selection for Choice fields
  [cillian]

- add support for the tus resumable file upload protocol
  [vangheem]

- handle unicode filenames for dexterity file uploads
  [vangheem]

- just always default to using File objects for uploads that aren't images.
  [vangheem]


1.4.0 (2013-11-24)
------------------

- add firstDay option to DatetimeWidgets
  [thet]

- removing bbb.py (SiteRSSItemsFieldWidget and SearchBoxViewlet)
  [garbas]

- For Archetypes DatetimeWidget, the value on pattern options is fixed, which
  was the time component missing.
  [thet]

- Fix the date/time value in pattern options for Archetypes DatetimeWidget.
  [thet]

- commenting out tinymce widget for the time being. will be back with next
  release.
  [garbas]

- Add robot tests for datetime widget
  [David Erni]

- fix saving dates in dexterity
  [vangheem]

- rework of base widget code. we should now share more code between at and dx
  [garbas]

- use ajax to grab query index options for querystring widget
  [vangheem]

- rename ajaxvocabulary to ajaxVocabulary to match mockup
  [vangheem]

- use select2 widget for ISiteSyndicationSettings
  [garbas]

- select2 widget should support initvaluemap  options OOTB
  [garbas]

- adding SyndicatableFeedItems to the permitted vocabularies list
  [garbas]

- fix VocabularyView to accept 1-based batch pages as per doc
  [djay]

- Change the start and end date fields of Products.ATContentTypes ATEvent
  types to use plone.app.widgets.
  [thet]

- For Dexterity DatetimeWidgetConverter, when converting to the field value,
  try to localize the value, if the old value is a timezone aware datetime
  object. It uses the 'timezone' attribute on the widget's context, if
  available, otherwise UTC.  We do not use the tzinfo object in the first
  place, because it might already be converted from user's input timezone to
  UTC, as it is the case with plone.app.event.
  [thet]

- Support query arguments for function based vocabularies.
  [thet]


1.3.3 (2013-09-11)
------------------

- fix formlib uberselectionwidget override
  [vangheem]

- SelectWidget fixes: support multiple-select; indicate the selected value.
  [davisagli]

- Don't include time in DateWidget.
  [davisagli]

- Allow to define a different vocabulary view for select widget
  [do3c]

- Don't do double batching in select widget code
  [do3cc]


1.3.2 (2013-08-12)
------------------

- Allow overriding with a custom vocabulary for Archetypes.
  [pbauer]

- Reuse z3c.form SelectWidget's logic for determing what items
  are available rather than recreating it incompletely.
  [davisagli]

- Use normal widget templates for z3c.form widgets in hidden mode.
  [davisagli]

- add formlib uber selection override for portlets
  [vangheem]


1.3.1 (2013-07-22)
------------------

- handle plone.app.relationfield not being installed
  [vangheem]

- handle unicode data in widgets beter
  [vangheem]


1.3 (2013-07-21)
----------------

- Additional set of widgets added and improved at Oshkosh and Bastille Sprint.
  [bunch of ppl]

- Fix bug where empty select elements rendered as <select/>
  [davisagli]

- Use normal widget templates for z3c.form widgets in display mode.
  [davisagli]

- For Archetypes subject fields, use the field's vocabulary_factory and fall
  back to 'plone.app.vocabularies.Keywords' if it's not present.
  [thet]

- Conditional include of collection ``QueryStringWidget`` which expects
  ``plone.app.contenttypes``.
  [saily]

- Restructure buildout to build an instance.
  [saily]

- Add travis icon
  [saily]

- Add german translation
  [saily]

- Fields and widgets demo gallery added [miohtama]


0.2 (2013-03-04)
----------------

 - add support for dexterity content types as well.
   [garbas]

 - using select2 pattern instead of textext pattern for select/autocomplete
   elements.
   [garbas]


0.1 (2013-01-31)
----------------

- initial release
  [garbas]
