*** Settings ***

Resource  common.robot
Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers


*** Variables ***

${form_url}  ${PLONE_URL}/@@select-widget-view

${mockup_bootstrap_class}  pat-select2

${select_field_name}  form.widgets.select_field
${list_field_name}  form.widgets.list_field

${input_search}  css=div#select2-drop div.select2-search input
${dropdown_multiple}  css=div#select2-drop ul.select2-results
${dropdown_select}  css=.select2-choice
${results_label}  css=.select2-result-label


*** Test Cases ***

The Select Widget has the class that bootstraps mockup JS
  Given a form
   Then the input fields have the mockup class

The Select Widget allows to select a single value
  Given a form
   When I select the option  3
   Then the widget shows the element  three

The Select Widget autocomplete function works
  Given a form
   When I type on the autocomplete field  wo
   Then the widget shows the element  two

The Select Multiple Widget allows to select multiple values
  Given a form

   When I click on the element  2
    And When I click on the element  1
   Then the widget shows two elements  five  four

The Select Multiple Widget autocomplete function works
  Given a form
   When I type on the multiple autocomplete field  s
   Then the widget shows one element  six


*** Keywords ***

# Given

a form
  Go to  ${form_url}

# When

I type on the autocomplete field
  [Arguments]  ${text}
  Wait For Condition  return $('.select2-choices:visible').size() > 0
  Open Dropdown  ${dropdown_select}  ${input_search}
  Input Text  ${input_search}  ${text}
  Click Element  ${results_label}

I type on the multiple autocomplete field
  [Arguments]  ${text}
  Wait For Condition  return $('.select2-choices:visible').size() > 0
  Execute Javascript  var $input = $('.select2-input'); $input.click().val('${text}'); var keyup = $.Event('keyup-change'); $input.trigger(keyup); return 0
  Click Element  ${results_label}

I select the option
  [Arguments]  ${index}
  Wait For Condition  return $('.select2-choices:visible').size() > 0
  Open Dropdown  ${dropdown_select}  ${input_search}
  Click Element  css=li.select2-results-dept-0:nth-child(${index})

I click on the element
  [Arguments]  ${index}
  Wait For Condition  return $('.select2-choices:visible').size() > 0
  Open Dropdown  css=#formfield-form-widgets-list_field input.select2-input  ${dropdown_multiple}
  Click Element  css=li.select2-results-dept-0:nth-child(${index})

# Then

the input fields have the mockup class
  Check Class On Element  ${select_field_name}
  Check Class On Element  ${list_field_name}

the widget shows the element
  [Arguments]  ${text}
  ${chosen_text} =  Get Text  css=.select2-chosen
  Should Be Equal  ${text}  ${chosen_text}  msg=${text} seems to not be selected

the widget shows two elements
  [Arguments]  ${first_string}  ${second_string}
  Text matches Input  li.select2-search-choice:nth-child(1) > div:nth-child(1)  ${first_string}
  Text matches Input  li.select2-search-choice:nth-child(2) > div:nth-child(1)  ${second_string}

the widget shows one element
  [Arguments]  ${string}
  Text matches Input  li.select2-search-choice:nth-child(1) > div:nth-child(1)  ${string}

# Custom keywords

Text matches Input
  [Arguments]  ${locator}  ${string}
  ${value} =  Get Text  css=${locator}
  Should Be Equal  ${string}  ${value}  msg=${string} seems to not be selected

Check Class On Element
  [Arguments]  ${locator}
  ${class_value} =  Get Element Attribute  identifier=${locator}@class
  Should Contain  ${class_value}  ${mockup_bootstrap_class}  msg=The CSS class is not ${mockup_bootstrap_class}, this could mean that p.a.widgets resources are not properly loaded

Open Dropdown
  [Arguments]  ${locator}  ${validaton}
  Click Element  ${locator}
  Wait Until Element is Visible  ${validaton}  error=The dropdown did not show up at location ${validaton}
