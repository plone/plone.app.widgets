*** Settings *****************************************************************

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  common.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open SauceLabs test browser
Test Teardown  Run keywords  Report test status  Close all browsers


*** Variables ****************************************************************

${xpath_date_field}  //input[contains(concat(' ',normalize-space(@class),' '),'pattern-pickadate-date')]
${xpath_time_field}  //input[contains(concat(' ',normalize-space(@class),' '),'pattern-pickadate-time')]
${xpath_month_select}  //select[contains(concat(' ',normalize-space(@class),' '),'picker__select--month')]
${xpath_year_select}  //select[contains(concat(' ',normalize-space(@class),' '),'picker__select--year')]
${xpath_day_list}  //div[contains(concat(' ',normalize-space(@class),' '),'picker__day')][contains(concat(' ',normalize-space(@class),' '),'picker__day--infocus')]
${xpath_time_list}  //li[contains(concat(' ',normalize-space(@class),' '),'picker__list-item')]
${xpath_date_input}  //div[contains(concat(' ',normalize-space(@class),' '),'pattern-pickadate-date-wrapper')]//input[@type='hidden']


*** Test Cases ***************************************************************

As a contributor I can enter the date and time
  Given I'm logged in as a 'Site Administrator'
    And Given I create a folder  My Folder
    And Given I open tab  Dates
   When I fill datetime field  Publishing Date  2010  1  30  4:00 a.m.
    And When I save
    And When I edit
    And When I open tab  Dates
   Then Page should contain datetime  Publishing Date  2010  1  30  4:00 a.m.


*** Keywords *****************************************************************

I fill datetime field
  [Arguments]  ${fieldlabel}  ${year}  ${month}  ${day}  ${time}
  Fill date field  ${fieldlabel}  ${year}  ${month}  ${day}
  Fill time field  ${fieldlabel}  ${time}

Fill date field
  [Arguments]  ${fieldlabel}  ${year}  ${month}  ${day}
  ${xpath_pattern} =  Convert to String  //div[label[text()[normalize-space(.)="${fieldlabel}"]]]
  ${month} =  Evaluate  str(int(${month}) - 1)

  Click Element  xpath=${xpath_pattern}${xpath_date_field}
  Select from list by value  xpath=${xpath_pattern}${xpath_month_select}  ${month}
  Select from list  xpath=${xpath_pattern}${xpath_year_select}  ${year}
  Click Element  xpath=${xpath_pattern}${xpath_day_list}[text()='${day}']

Fill time field
  [Arguments]  ${fieldlabel}  ${time}
  ${xpath_pattern} =  Convert to String  //div[label[text()[normalize-space(.)="${fieldlabel}"]]]
  Click Element  xpath=${xpath_pattern}${xpath_time_field}
  ${xpath_time} =  Convert to String  ${xpath_pattern}${xpath_time_list}[text()='${time}']
  Wait until page contains Element  xpath=${xpath_time}
  Click Element  xpath=${xpath_time}

Page should contain datetime
  [Arguments]  ${fieldlabel}  ${year}  ${month}  ${day}  ${time}
  Page should contain date   ${fieldlabel}  ${year}  ${month}  ${day}
  Page should contain time  ${fieldlabel}  ${time}

Page should contain date
  [Arguments]  ${fieldlabel}  ${year}  ${month}  ${day}
  ${xpath_pattern} =  Convert to String  //div[label[text()[normalize-space(.)="${fieldlabel}"]]]
  ${expected_date} =  Evaluate  datetime.date(${year}, ${month}, ${day}).strftime('%Y-%m-%d')  modules=datetime
  ${actual_date} =  Get Value  ${xpath_pattern}${xpath_date_input}
  Should be equal  ${expected_date}  ${actual_date}

Page should contain time
  [Arguments]  ${fieldlabel}  ${time}
  Page should contain  ${time}

