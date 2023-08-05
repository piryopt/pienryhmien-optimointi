*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${SERVER}  127.0.0.1:5000/
${BROWSER}  headlessfirefox
${DELAY}  0.0 seconds
${HOME_URL}  http://${SERVER}
${LOGOUT URL}  http://${SERVER}/auth/logout
${CREATE SURVEY URL}  http://${SERVER}/surveys/create

${AD_LOGIN_BUTTON}    xpath=//button[@type='submit' and contains(text(),'Login')]
${FIRST_TIME_LOGIN_ACCEPT}  xpath=//button[@type='submit' and contains(text(),'Accept')]

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
