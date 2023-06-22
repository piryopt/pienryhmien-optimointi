*** Settings ***
Documentation  Testing
Library  SeleniumLibrary

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0.0 seconds
${HOME URL}  http://${SERVER}
${REGISTER URL}  http://${SERVER}/register
${LOGIN URL}  http://${SERVER}/login
${CREATE SURVEY URL}  http://${SERVER}/create_survey
${PREVIOUS SURVEYS URL}  http://${SERVER}/previous_surveys
${LOGOUT URL}  http://${SERVER}/logout

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}

Main Page Should Be Open
    Page Should Contain  Index
    Page Should Contain  Hello
    Page Should Contain  Kokeile luoda dataa
    Page Should Contain  Kokeile valmiilla datalla

Register Page Should Be Open
	Page Should Contain  Register

Login Page Should Be Open
	Page Should Contain  Login

Create Survey Page Should Be Open
	Page Should Contain  Luo uusi kysely
    Page Should Contain  Priorisoitavat ryhmät

Previous Surveys Page Should Be Open
	Page Should Contain  Aiemmat kyselyt
    Page Should Contain  Kyselyn nimi
    Page Should Contain  Kyselyn tila

Go To Main Page
    Go To  ${HOME URL}

Go To Register Page
    Go To  ${REGISTER URL}

Go To Login Page
    Go To  ${LOGIN URL}

Go To Create Survey Page
    Go To  ${CREATE SURVEY URL}

Go To Previous Surveys Page
    Go To  ${PREVIOUS SURVEYS URL}

Go To Logout Page
    Go To  ${LOGOUT URL}
