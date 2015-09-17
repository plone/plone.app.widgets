Changelog
=========

1.8.1 (unreleased)
------------------

- Allow time options to be customized for DatetimeWidget.
  [thet]

- add registry settings for pickadate options (Taken from Plone 5.0
  plone.patternoptions)
  [petschki]

- Let ``@@getVocabulary`` return the vocabulary's value instead of the token
  for the id in the result set. The token is binary encoded and leads to
  encoding errors when selecting a value with non-ASCII data from vocabulary
  list in a select2 based widget.
  Fixes: https://github.com/plone/Products.CMFPlone/issues/650
  [thet]


1.8.0 (2015-05-25)
------------------

- Register the ``plonejsi18n`` view for all contexts, so that it can be called
  also on the Zope root. If no base url is found, it's called on "/".
  [thet]

- Allow ``getVocabulary`` calls without a fieldname on INavigationRoot instead
  of IPloneSiteRoot. This adds compatibility for Lineage based subsites.
  [thet]

- Use widget bundle from mockup's build directory, if mockup is installed. In
  this case, you need to build the widgets bundle in the mockup directory.
  [thet]

- Implement selectableTypes for the RelatedItems pattern
  [petschki]

- Include TinyMCE languages from mockup.
  [petschki]

- Change TinyMCE pattern options: Add the folderTypes list to the RelatedItems
  widget in TinyMCE (fixes issues with the tinymce configuration option
  ``containsobjects`` not being respected), set the RelatedItems widget mode to
  browse and set the basePath to the current folder (starts the RelatedItems
  widget in the insert link and image dialogs from the current folder, where
  one can browse down the content tree).
  [thet]

- Update the mockup widget bundle.
  [thet]

- Allow the JavaScript and CSS resources to be cachable and cookable. Set
  applyPrefix for the CSS resource.
  [thet]

- Add the ``form_tabbing.js`` and ``toc.js`` scripts to the deprecated bundles.
  They're made obsolete by ``mockup-patterns-autotoc``.
  [thet]

- Include TinyMCE configuration from plone control panel (unfinished)
  [frisi, petschki]

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
