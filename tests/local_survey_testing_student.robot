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

*** Test Cases ***
Login As Student
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Login And Go To Main Page  robottiStudent  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely

Go To Create Survey Page As Student
    Go To Create Survey Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely

