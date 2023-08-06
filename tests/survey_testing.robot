*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${SERVER}  127.0.0.1:5000
${BROWSER}  firefox
${DELAY}  0.1 seconds
${HOME_URL}  http://${SERVER}/
${LOGOUT URL}  http://${SERVER}/auth/logout
${CREATE SURVEY URL}  http://${SERVER}/surveys/create
${SURVEYS URL}  http://${SERVER}/surveys

${FILE_UPLOAD_BUTTON}  css=[type='file']

${AD_LOGIN_BUTTON}    xpath=//button[@type='submit' and contains(text(),'Login')]
${FIRST_TIME_LOGIN_ACCEPT}  xpath=//button[@type='submit' and contains(text(),'Accept')]
${CREATE_NEW_SURVEY_BUTTON}  xpath=//button[@type='submit' and contains(text(),'Luo kysely')]

*** Test Cases ***
Login As Teacher
    Logout And Go To Login
    Input Login Credentials  robottiTeacher  moi123
    # first time logging in real AD login asks the do you consent
    # to disclosing this information etc. this clicks that button
    Run Keyword And Ignore Error  Click Element  ${FIRST_TIME_LOGIN_ACCEPT}
    Wait Until Location Is  ${HOME_URL}
    Go To Main Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely

Create Survey As Teacher Manually
    Go To Create Survey Page
    Title Should Be  Luo uusi kysely - Jakaja
    Input Text  groupname  Robot created test
    Input Text  startdate  01.08.2023
    Input Text  starttime  01:01
    Input Text  enddate  01.08.2024
    Input Text  endtime  02:02
    # no description because reasons
    Set Focus To Element  id:minchoices
    Input Text  minchoices  2
    Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey1.csv
    Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    Click Element  ${CREATE_NEW_SURVEY_BUTTON}
    Go To  ${SURVEYS URL}
    Page Should Contain  Robot created test

  
Login As Student
    Logout And Go To Login
    Input Login Credentials  robottiStudent  moi123
    Run Keyword And Ignore Error  Click Element  ${FIRST_TIME_LOGIN_ACCEPT}
    Wait Until Location Is  ${HOME_URL}
    Go To Main Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely

Go To Create Survey Page As Student
    Go To Create Survey Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely
