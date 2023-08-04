*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Library  Dialogs

*** Variables ***
${MOCK_LOGIN_BUTTON}    xpath=//button[@type='submit' and contains(text(),'Kirjaudu sisään')]

*** Test Cases ***
Open Main Page As Teacher Test
    Go To Logout Page
    Go To Login Page
    Set Name  TestiOpettaja
    Set Email  opettaja.testi@helsinki.fi
    Set Role Number  1
    Click Element  ${MOCK_LOGIN_BUTTON}
    Page Should Contain  Luo uusi kysely

Open Main Page As Student Test
    Go To Logout Page
    Go To Login Page
    Set Name  TestiOpettaja
    Set Email  opettaja.adsdsadsa@helsinki.fi
    Set Role Number  0
    Click Element  ${MOCK_LOGIN_BUTTON}
    Page Should Not Contain  Luo uusi kysely
    Page Should Contain  Näytä vanhat kyselyt


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

Set Info1
    [Arguments]  ${choiceInfo1}
    Input Text  choiceInfo1  ${choiceInfo1}

Set Info2
    [Arguments]  ${choiceInfo2}
    Input Text  choiceInfo2  ${choiceInfo2}
