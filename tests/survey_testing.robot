*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${REGISTERBUTTON}    xpath=//button[@type='submit' and contains(text(),'Luo tunnus')]
${LOGINBUTTON}    xpath=//button[@type='submit' and contains(text(),'Kirjaudu')]
${NEWSURVEY}    xpath=//button[@type='submit' and contains(text(),'Luo kysely')]

*** Test Cases ***


*** Keywords ***
Set Email
    [Arguments]  ${email}
    Input Text  email  ${email}

Set Name
    [Arguments]  ${name}
    Input Text  name  ${name}

Set Student_number
    [Arguments]  ${student_number}
    Input Text  student_number  ${student_number}

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
