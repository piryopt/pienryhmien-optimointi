*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${REGISTERBUTTON}    xpath=//button[@type='submit' and contains(text(),'Luo tunnus')]
${LOGINBUTTON}    xpath=//button[@type='submit' and contains(text(),'Kirjaudu')]
${NEWSURVEY}    xpath=//button[@type='submit' and contains(text(),'Luo kysely')]

*** Test Cases ***
Open Main Page Test
    Go To Main Page
    Main Page Should Be Open

Open Register Page Test
    Go To Register Page
    Register Page Should Be Open

Open Login Page Test
    Go To Login Page
    Login Page Should Be Open

Register New Student Test
    Go To Register Page
    Register Page Should Be Open
    Set Email  studenttrobot@robot.com
    Set Name  Robot McRobot
    Set Student_number  010101010
    Select From List By Value  name:isteacher  student
    Click Element  ${REGISTERBUTTON}
    Login Page Should Be Open

Register New Teacher Test
    Go To Register Page
    Register Page Should Be Open
    Set Email  testtrobot@robot.com
    Set Name  Roboty McRobotface
    Set Student_number  010101011
    Select From List By Value  name:isteacher  teacher
    Click Element  ${REGISTERBUTTON}
    Login Page Should Be Open

Login With Incorrect Credentials Test
    Go To Login Page
    Login Page Should Be Open
    Set Email  norobott@robot.com
    Click Element  ${LOGINBUTTON}
    Login Page Should Be Open

Login Teacher Test
    Go To Login Page
    Login Page Should Be Open
    Set Email  testtrobot@robot.com
    Click Element  ${LOGINBUTTON}
    Main Page Should Be Open

Open Previous Surveys Page Test
    Go To Previous Surveys Page
    Previous Surveys Page Should Be Open

Logout Works Test
    Go To Main Page
    Main Page Should Be Open
    Go To Logout Page
    Main Page Should Be Open

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
