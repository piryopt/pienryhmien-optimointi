*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${SERVER}  piryopt.ext.ocp-test-0.k8s.it.helsinki.fi
${BROWSER}  headlessfirefox
${DELAY}  0.0 seconds
${HOME_URL}  https://${SERVER}/
${LOGOUT URL}  http://${SERVER}/auth/logout
${CREATE SURVEY URL}  http://${SERVER}/surveys/create
${SURVEYS URL}  http://${SERVER}/surveys

${FILE_UPLOAD_BUTTON}  css=[type='file']

${SURVEY NAME}  Testikysely paskaaaaaa

${AD_LOGIN_BUTTON}    xpath=//button[@type='submit' and contains(text(),'Login')]
${FIRST_TIME_LOGIN_ACCEPT}  xpath=//button[@type='submit' and contains(text(),'Accept')]
${CREATE_NEW_SURVEY_BUTTON}  xpath=//button[@type='submit' and contains(text(),'Luo kysely')]
${SURVEY HREF}  xpath=//a[contains(text(), '${SURVEY NAME}')]

*** Test Cases ***
Login As Teacher
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Login And Go To Main Page  robottiTeacher  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely

Create Survey As Teacher From CSV
    Go To Create Survey Page
    Title Should Be  Luo uusi kysely - Jakaja
    Set Create Survey Mandatory Fields  ${SURVEY NAME}  01.08.2023  01:01  01.08.2024  02:02  2
    Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey1.csv
    Wait Until Page Contains  Päiväkoti Gehenna
    Wait Until Page Contains Element  ${CREATE_NEW_SURVEY_BUTTON}
    Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    Click Element  ${CREATE_NEW_SURVEY_BUTTON}
    Go To  ${SURVEYS URL}
    Page Should Contain  ${SURVEY NAME}
    Wait Until Page Contains Element  ${SURVEY HREF}
    Set Focus To Element  ${SURVEY HREF}
    Click Element  ${SURVEY HREF}
    Page Should Contain  Päiväkoti Toivo
    Page Should Contain  Päiväkoti Gehenna

Login As Student
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Login And Go To Main Page  robottiStudent  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely

Go To Create Survey Page As Student
    Go To Create Survey Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely
