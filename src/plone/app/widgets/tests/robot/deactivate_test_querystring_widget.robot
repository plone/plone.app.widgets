*** Settings ***

Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot
Resource  common.robot

Test Setup  Run Keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown

*** Variables ***
${querywidget_selector}  \#formfield-form-widgets-ICollection-query

*** Test Cases ***

Querystring Widget rows appear and disappear correctly
  Given I'm logged in as a 'Site Administrator'
    And I create a collection  My Collection
        Wait For Condition  return !!document.querySelector('body.patterns-loaded')
        Wait until page contains Element  css=${querywidget_selector} .querystring-criteria-wrapper:nth-child(1)
        Wait Until Page Does Not Contain Element  css=${querywidget_selector} .querystring-criteria-wrapper:nth-child(2)
   When I select criteria index in row  1  Expiration date
        Wait until page contains Element  css=${querywidget_selector} .querystring-criteria-wrapper:nth-child(2)
   When Click Element  css=${querywidget_selector} .querystring-criteria-wrapper:nth-child(2) .querystring-criteria-remove
        Wait until page contains Element  css=${querywidget_selector} .querystring-criteria-wrapper:nth-child(2)
   When Click Element  css=${querywidget_selector} .querystring-criteria-wrapper:nth-child(1) .querystring-criteria-remove
        Wait Until Page Does Not Contain Element  css=${querywidget_selector} .querystring-criteria-wrapper:nth-child(2)


Querystring Widget date criteria master/select behaviour is correct ***
  Given I'm logged in as a 'Site Administrator'
    And I create a collection  My Collection
   When I select criteria index in row  1  Expiration date
        Date criteria operators are functional  1
   When I select criteria index in row  1  Event end date
        Date criteria operators are functional  1
   When I select criteria index in row  1  Effective date
        Date criteria operators are functional  1
   When I select criteria index in row  1  Event start date
        Date criteria operators are functional  1
   When I select criteria index in row  1  Creation date
        Date criteria operators are functional  1
   When I select criteria index in row  1  Modification date
        Date criteria operators are functional  1


Querystring Widget text criteria master/select behaviour is correct
  Given I'm logged in as a 'Site Administrator'
    And I create a collection  My Collection
   When I select criteria index in row  1  Description
        Operator slave field becomes visible  1  .querystring-criteria-value-StringWidget
   When I select criteria index in row  1  Title
        Operator slave field becomes visible  1  .querystring-criteria-value-StringWidget
   When I select criteria index in row  1  Searchable text
        Operator slave field becomes visible  1  .querystring-criteria-value-StringWidget
   When I select criteria index in row  1  Tag
        Operator slave field becomes visible  1  .querystring-criteria-value-MultipleSelectionWidget


Querystring Widget metadata criteria master/select behaviour is correct
  Given I'm logged in as a 'Site Administrator'
    And I create a collection  My Collection
   When I select criteria index in row  1  Type
        Operator slave field becomes visible  1  .querystring-criteria-value-MultipleSelectionWidget
   When I select criteria index in row  1  Short name
        Operator slave field becomes visible  1  .querystring-criteria-value-StringWidget
   When I select criteria index in row  1  Creator
    And I select criteria operator in row  1  Matches any of
        Operator slave field becomes visible  1  .querystring-criteria-value-MultipleSelectionWidget
   When I select criteria index in row  1  Location
        Operator slave field becomes visible  1  .querystring-criteria-value-ReferenceWidget
   When I select criteria index in row  1  Location
    And I select criteria operator in row  1  Advanced Mode
    And I select criteria operator in row  1  Relative Path
        Operator slave field becomes visible  1  .querystring-criteria-value-RelativePathWidget
   When I select criteria index in row  1  Review state
        Operator slave field becomes visible  1  .querystring-criteria-value-MultipleSelectionWidget


Collection Creation works
  Given I'm logged in as a 'Site Administrator'
    And I create a collection  My Collection
   When I select criteria index in row  1  Location
    And I select criteria operator in row  1  Advanced Mode
    And I save
        Wait until page contains Element  jquery=.contenttype-collection:contains(My Collection)


*** Keywords ***

I select criteria index in row
  [Arguments]  ${number}  ${label}
  ${criteria_row} =  Convert to String  ${querywidget_selector} .querystring-criteria-wrapper:nth-child(${number})
  Wait For Then Click Element  css=${criteria_row} .querystring-criteria-index .select2-container a
  Wait until Element is Visible  css=#select2-drop .select2-input
  Input Text  css=#select2-drop .select2-input  text=${label}
  Press Key  css=#select2-drop .select2-input  \\13

I select criteria operator in row
  [Arguments]  ${number}  ${label}
  ${criteria_selector} =  Convert to String  ${querywidget_selector} .querystring-criteria-wrapper:nth-child(${number}) .querystring-criteria-operator .select2-container .select2-choice
  Click Link  css=${criteria_selector}
  Wait until Element is Visible  css=#select2-drop
  Wait For Then Click Element  xpath=//div[@id="select2-drop"]/ul[@class="select2-results"]//*[contains(text(), "${label}")]
  Wait until Element is not Visible  css=#select2-drop

Operator slave field becomes visible
  [Arguments]  ${number}  ${selector}
  ${criteria_row} =  Convert to String  ${querywidget_selector} .querystring-criteria-wrapper:nth-child(${number})
  Wait until page contains Element  css=${criteria_row} .querystring-criteria-value ${selector}

Date criteria operators are functional
  [Arguments]  ${number}
  I select criteria operator in row  ${number}  Today
  I select criteria operator in row  ${number}  Within last
  Operator slave field becomes visible  ${number}  .querystring-criteria-value-RelativeDateWidget
  I select criteria operator in row  ${number}  Before date
  Operator slave field becomes visible  ${number}  .querystring-criteria-value-DateWidget
  I select criteria operator in row  ${number}  After date
  Then Operator slave field becomes visible  ${number}  .querystring-criteria-value-DateWidget
  I select criteria operator in row  ${number}  Within next
  Then Operator slave field becomes visible  ${number}  .querystring-criteria-value-RelativeDateWidget
  I select criteria operator in row  ${number}  Before today
  I select criteria operator in row  ${number}  Between dates
  Then Operator slave field becomes visible  ${number}  .querystring-criteria-value-DateRangeWidget
