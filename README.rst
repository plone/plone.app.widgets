``plone.app.widgets`` is a revamp of plone widgets. It does this by overriding
the widgets of some of the fields in plone.

Widgets that are overridden in ``Edit`` forms are:

- ``subject``
- ``language``
- ``effectiveDate``
- ``expirationDate``
- ``contributrors``
- ``creators``

Currently ``plone.app.widgets`` only works with Archetypes, but Dexterity
support is planned in next release.

All client side code (javascript/css/images) is done and tested as part of
`Plone Mockup`_ project.

Any feature / bug / compliment please insert in `issue tracker`_.

.. _`Plone Mockup`: https://plone.github.com/mockup
.. _`issue tracker`: https://github.com/plone.app.widgets/issues
