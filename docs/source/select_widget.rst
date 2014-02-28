=============
Select Widget
=============

The ``Select Widget`` enhances the default drop down menu with a nice wrapper
that adds autocomplete functionality.

It comes with two flavours: single select or multi select.

.. image:: widget-select-single-open.png

See below on how to use it on your projects.

There are three steps to test the integration of a widget within your project:

- :ref:`widget-select-python-label`
- :ref:`widget-select-zcml-label`
- :ref:`widget-select-test-label`


.. _widget-select-python-label:

Python
======

To use the widget we need to create an schema interface that defines fields
where the ``SelectWidget`` is assigned:

.. code:: python

    # -*- coding: utf-8 -*-
    from plone.app.widgets.dx import SelectWidget
    from plone.autoform import directives
    from zope.interface import Interface
    from zope.schema import Choice
    from zope.schema import List


    class ITestSelectWidgetSchema(Interface):

        directives.widget('select_field', SelectWidget)
        select_field = Choice(
            title=u'Select Widget',
            values=['one', 'two', 'three', ]
        )

        directives.widget('list_field', SelectWidget)
        list_field = List(
            title=u'Select Multiple Widget',
            value_type=Choice(values=['four', 'five', 'six', ]),
        )

.. note::
   To use a specific widget for a field
   ``plone.autoform.directives.widget`` is used.

.. note::
   When a field is of type ``zope.schema.List`` and ``SelectWidget`` is used,
   it automatically defaults to its multiple flavour.

Next we need to create a form that uses the schema interface created above:

.. code:: python

    # -*- coding: utf-8 -*-
    from plone.autoform.form import AutoExtensibleForm
    from z3c.form import form


    class TestSelectWidgetForm(AutoExtensibleForm, form.EditForm):

        schema = ITestSelectWidgetSchema
        ignoreContext = True


Finally, and only for testing purposes, we need to create a testing layer that
uses this form:

.. code:: python

    # -*- coding: utf-8 -*-
    from plone.app.testing.layers import FunctionalTesting
    from plone.app.widgets.testing import PloneAppWidgetsLayer
    from plone.app.widgets.testing import PLONEAPPWIDGETS_FIXTURE_DX


    class SelectWidgetLayer(PloneAppWidgetsLayer):

        defaultBases = (PLONEAPPWIDGETS_FIXTURE_DX, )

        def setUpZope(self, app, configurationContext):
            super(SelectWidgetLayer, self).setUpZope(app, configurationContext)
            import plone.app.widgets.tests
            from zope.configuration import xmlconfig
            xmlconfig.file('configure.zcml', plone.app.widgets.tests,
                           context=configurationContext)


    SELECT_WIDGET_FIXTURE = SelectWidgetLayer()
    SELECT_WIDGET_ROBOT_TESTING = FunctionalTesting(
        bases=(SELECT_WIDGET_FIXTURE,
               z2.ZSERVER_FIXTURE),
        name='SelectWidgetLayer:Robot')

.. note::
   The ``xmlconfig`` method used here is to be able to load the ZCML defined
   in the next step.


.. _widget-select-zcml-label:

ZCML
====

To be able to use the form created in the previous step, register a view that
uses it.

.. note::
   Usually, if the schema interface is bound to a content type this step is
   not needed, as add/edit forms are automatically registered.

.. code:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">

      <browser:page
        for="*"
        name="select-widget-view"
        class="..testing.TestSelectWidgetForm"
        permission="zope2.View"
        />

    </configure>


.. _widget-select-test-label:

Test
====

To test that the widget works as expected `Robot Framework`_ is used. A
complete example can be seen in `p.a.widgets select widget example test`_.

.. code:: robotframework
   :class: hidden

   *** Settings ***

   Resource  plone/app/robotframework/server.robot

   Library  Selenium2Screenshots

   Suite Setup  Setup Plone Site with p.a.widgets
   Suite Teardown  Run keywords  Teardown Plone site  Close all browsers


   *** Variables ***

   ${form_url}  ${PLONE_URL}/@@select-widget-view

   ${select_field_name}  form.widgets.select_field
   ${list_field_name}  form.widgets.list_field

   ${input_search}  css=div#select2-drop div.select2-search input
   ${results_label}  css=.select2-result-label

After selecting an element:

.. image:: widget-select-single-one-value.png

After selecting multiple elements:

.. image:: widget-select-multiple-value.png


Autocompletion:

.. image:: widget-select-autocomplete.png

.. code:: robotframework

   *** Test Cases ***

   Open Plone with a form
     Given a form

   Show the dropdown and select an element
     Open Dropdown  css=.select2-choice  css=#select2-drop div.select2-search input
     Capture and crop page screenshot  widget-select-single-open.png  css=#form
     Input Text  css=div#select2-drop div.select2-search input  t
     Capture and crop page screenshot  widget-select-autocomplete.png  css=#form
     Click Element  css=li.select2-results-dept-0:nth-child(2)
     Capture and crop page screenshot  widget-select-single-one-value.png  css=#form

   Select multiple elements
     Open Dropdown  css=.select2-input  css=#select2-drop ul.select2-results
     Click Element  css=li.select2-results-dept-0:nth-child(2)
     Open Dropdown  css=.select2-input  css=#select2-drop ul.select2-results
     Click Element  css=li.select2-results-dept-0:nth-child(1)
     Capture and crop page screenshot  widget-select-multiple-value.png  css=#form

   *** Keywords ***

   Setup Plone Site with p.a.widgets
     Setup Plone site  plone.app.widgets.testing.SELECT_WIDGET_ROBOT_TESTING
     Set window size  800  600

   a form
     Go to  ${form_url}

   Open Dropdown
     [Arguments]  ${locator}  ${validaton}
     Click Element  ${locator}
     Wait Until Element is Visible  ${validaton}


.. _Robot Framework: http://robotframework.org/
.. _p.a.widgets select widget example test: https://github.com/plone/plone.app.widgets/blob/master/plone/app/widgets/tests/robot_widgets/test_select_widget.robot
