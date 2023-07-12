*** Settings ***
Documentation  Testing
Library  SeleniumLibrary

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlessfirefox
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
    Set Window Size  1920  1080
    Set Selenium Speed  ${DELAY}

Main Page Should Be Open
    Page Should Contain  Tervetuloa
    Page Should Contain  Näytä vanhat kyselyt

Register Page Should Be Open
	Page Should Contain  Nimi
    Page Should Contain  Opiskelijanumero
    Page Should Contain  Rooli

Login Page Should Be Open
	Page Should Contain  Kirjaudu sisään

Create Survey Page Should Be Open
	Page Should Contain  Luo uusi kysely
    Page Should Contain  Priorisoitavat ryhmät

Previous Surveys Page Should Be Open
	Page Should Contain  Aiemmat kyselyt
    Page Should Contain  Nimi
    Page Should Contain  Kyselyn tila
    Page Should Contain  Toiminnot

Excel Page Should Be Open
    Title Should Be     Tulokset - Jakaja
    Page Should Contain     Lajittelun tulokset
    Page Should Contain     Ryhmänvalintojen keskiarvo
    Page Should Contain     1. valintaansa sijoitetut opiskelijat:
    Page Should Contain     2. valintaansa sijoitetut opiskelijat:
    Page Should Contain     3. valintaansa sijoitetut opiskelijat: 
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
