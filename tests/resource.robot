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
${EXCEL URL}  http://${SERVER}/excel
${TOY DATA FORM}  http://${SERVER}/input
${TOY DATA RESULTS URL}  http://${SERVER}/results

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

Excel Page Should Be Open
    Title Should Be     Tulokset - Piryopt
    Page Should Contain     Lajittelun tulokset
    Page Should Contain     Ryhmänvalintojen keskiarvo
    Page Should Contain     1.0. valinta:
    Page Should Contain     2.0. valinta:
    Page Should Contain     3.0. valinta: 
    Page Should Contain     aikaa kului
    Page Should Contain     Opiskelijat on lajiteltu ryhmiin seuraavasti

Toy Data Input Page Should Be Open
    Page Should Contain  Luo satunnaista testidataa
    Page Should Contain  Ryhmien lukumäärä
    Page Should Contain  Ryhmien maksimikoko

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

Go To Excel Page
    Go To  ${EXCEL URL}

Go To Toy Data Input Page
    Go To  ${TOY DATA FORM}

Go To Toy Data Results Page
    Go To  ${TOY DATA RESULTS URL}

