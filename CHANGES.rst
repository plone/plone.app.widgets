Changelog
=========


1.3.3 (2013-09-11)
------------------

- fix formlib uberselectionwidget override
  [vangheem]

- SelectWidget fixes: support multiple-select; indicate the selected value.
  [davisagli]

- Don't include time in DateWidget.
  [davisagli]

- Allow to define a different vocabulary view for select widget
  [do3c]]

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
