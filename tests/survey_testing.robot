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

Open Previous Surveys Page Test
    Go To Previous Surveys Page
    Previous Surveys Page Should Be Open

Register New Student Test
    Go To Register Page
    Register Page Should Be Open
    Set Email  studenttrobot@robot.com
    Set Firstname  Robot
    Set Lastname  McRobot
    Set Student_number  010101010
    Set Password1  robot4lyfe
    Set Password2  robot4lyfe
    Select From List By Value  name:isteacher  student
    Click Element  ${REGISTERBUTTON}
    Login Page Should Be Open

Register New Teacher Test
    Go To Register Page
    Register Page Should Be Open
    Set Email  testtrobot@robot.com
    Set Firstname  Roboty
    Set Lastname  McRobotface
    Set Student_number  010101011
    Set Password1  robot4lyfe
    Set Password2  robot4lyfe
    Select From List By Value  name:isteacher  teacher
    Click Element  ${REGISTERBUTTON}
    Login Page Should Be Open

Login With Incorrect Credentials Test
    Go To Login Page
    Login Page Should Be Open
    Set Email  norobott@robot.com
    Set Password  robot4lyfe
    Click Element  ${LOGINBUTTON}
    Login Page Should Be Open

Login Teacher Test
    Go To Login Page
    Login Page Should Be Open
    Set Email  testtrobot@robot.com
    Set Password  robot4lyfe
    Click Element  ${LOGINBUTTON}
    Main Page Should Be Open

Create New Survey Test
    Go To Create Survey Page
    Create Survey Page Should Be Open
    Set Surveyname  Best robots
    Set Choicename  Tars
    Set Choicemaxspaces  10
    Set Info1  My honesty threshold is set too high
    Set Info2  Interstellar
    Click Button  addchoice
    Set Choicename  Iron Giant
    Set Choicemaxspaces  10
    Set Info1  Superman
    Set Info2  The Iron Giant
    Click Button  addchoice
    Set Choicename  T-800
    Set Choicemaxspaces  10
    Set Info1  I'll be back
    Set Info2  The Terminator
    Click Button  addchoice
    Set Choicename  Megatron
    Set Choicemaxspaces  10
    Set Info1  NOBODY SUMMONS MEGATRON
    Set Info2  Transformers
    Click Button  addchoice
    Set Choicename  Starscream
    Set Choicemaxspaces  10
    Set Info1  FeelsBadMan
    Set Info2  Transformers
    Click Button  addchoice
    Click Element  ${NEWSURVEY}
    Go To Previous Surveys Page
    Page Should Contain  Best robots

Logout Works Test
    Go To Main Page
    Main Page Should Be Open
    Go To Logout Page
    Main Page Should Be Open

*** Keywords ***
Set Email
    [Arguments]  ${email}
    Input Text  email  ${email}

Set Firstname
    [Arguments]  ${firstname}
    Input Text  firstname  ${firstname}

Set Lastname
    [Arguments]  ${Lastname}
    Input Text  lastname  ${lastname}

Set Student_number
    [Arguments]  ${student_number}
    Input Text  student_number  ${student_number}

Set Password
    [Arguments]  ${password}
    Input Text  password  ${password}

Set Password1
    [Arguments]  ${password1}
    Input Text  password1  ${password1}

Set Password2
    [Arguments]  ${password2}
    Input Text  password2  ${password2}

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