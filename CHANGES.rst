Changelog
=========


1.4.0 (2013-11-24)
------------------

- add firstDay option to DatetimeWidgets
  [thet]

- removing bbb.py (SiteRSSItemsFieldWidget and SearchBoxViewlet)
  [garbas]

- For Archetypes DatetimeWidget, the value on pattern options is fixed, which
  was the time component missing.
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

- Fix the date/time value in pattern options for Archetypes DatetimeWidget.
  [thet]

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
