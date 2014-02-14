*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/saucelabs.robot

Library  Remote  ${PLONE_URL}/RobotRemote

*** Keywords ***

# ----------------------------------------------------------------------------
# Login/Logout
# ----------------------------------------------------------------------------

I'm logged in as a '${ROLE}'
    Enable autologin as  ${ROLE}
    Go to  ${PLONE_URL}

# ----------------------------------------------------------------------------
# Navigation
# ----------------------------------------------------------------------------

I open tab
  [Arguments]  ${tabname}
  Click link  ${tabname}

I save
  Click button  Save
  Wait until page contains  Item created

I edit
  Click link  css=#contentview-edit a
  Wait until page contains Element  id=form-buttons-save

# ----------------------------------------------------------------------------
# Content
# ----------------------------------------------------------------------------

I create a collection
  [Arguments]  ${title}
  Go to  ${PLONE_URL}/++add++Collection
  Wait until page contains  Add Collection
  Input text  name=form.widgets.IDublinCore.title  ${title}

I create a folder
  [Arguments]  ${title}
  Go to  ${PLONE_URL}/++add++Folder
  Wait until page contains  Add Folder
  Input text  name=form.widgets.IDublinCore.title  ${title}
