*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Library  Dialogs

*** Variables ***
${SERVER}  127.0.0.1:5000/
${BROWSER}  headlessfirefox
${DELAY}  0.0 seconds
${HOME_URL}  http://${SERVER}

${AD_LOGIN_BUTTON}    xpath=//button[@type='submit' and contains(text(),'Login')]

*** Test Cases ***
Login As Teacher
    Go To Logout Page
    Go To Main Page
    Input Text  username  outi1
    Input Text  password  moi123
    Click Element  ${AD_LOGIN_BUTTON}
    Wait Until Location Is  ${HOME_URL}
    Go To Main Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely

Login As Student
    Go To Logout Page
    Go To Main Page
    Input Text  username  olli1
    Input Text  password  moi123
    Click Element  ${AD_LOGIN_BUTTON}
    Wait Until Location Is  ${HOME_URL}
    Go To Main Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely




*** Keywords ***
Set Email
    [Arguments]  ${email}
    Input Text  email  ${email}

Set Name
    [Arguments]  ${name}
    Input Text  name  ${name}

Set Role Number
    [Arguments]  ${student_number}
    Input Text  role  ${student_number}

Set Surveyname
    [Arguments]  ${groupname}
    Input Text  groupname  ${groupname}

Set Choicename
    [Arguments]  ${choicename}
    Input Text  choiceName  ${choiceName}

Set Choicemaxspaces
    [Arguments]  ${choiceMaxSpaces}
    Input Text  choiceMaxSpaces  ${choiceMaxSpaces}
