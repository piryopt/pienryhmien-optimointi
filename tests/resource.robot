*** Settings ***
Documentation  Testing
Library  SeleniumLibrary
Library  OperatingSystem


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


# NEW

Input Login Credentials
    [Arguments]  ${username}  ${password}
    Input Text  username  ${username}
    Input Text  password  ${password}
    Click Element  ${AD_LOGIN_BUTTON}

Logout And Go To Login
    [Documentation]  Call when changing user
    Go To Logout Page
    Go To Main Page

Login And Go To Main Page
    [Arguments]  ${username}  ${password}
    Logout And Go To Login
    Input Login Credentials  ${username}  ${password}
    Run Keyword And Ignore Error  Click Element  ${FIRST_TIME_LOGIN_ACCEPT}
    Wait Until Location Is  ${HOME_URL}
    Go To Main Page

Set Create Survey Mandatory Fields
    [Documentation]  Call when in create survey page
    [Arguments]  ${surveyname}  ${startdate}  ${starttime}  ${enddate}  ${endtime}  ${minchoices}
    Input Text  groupname  ${surveyname}
    Input Text  startdate  ${startdate}
    Input Text  starttime  ${starttime}
    Input Text  enddate  ${enddate}
    Input Text  endtime  ${endtime}
    Set Focus To Element  id:minchoices
    Input Text  minchoices  ${minchoices}

Drag To Top Of Choices
    [Arguments]  ${choice}
    ${temp}=  Get Vertical Position  ${choice}
    ${y cord}=  Evaluate  (-1) * (${temp} - 100)
    Drag And Drop By Offset  ${choice}  -300  ${y cord}
    
Go To Main Page
    Go To  ${HOME URL}

Go To Register Page
    Go To  ${REGISTER URL}

Go To Create Survey Page
    Go To  ${CREATE SURVEY URL}

Go To Previous Surveys Page
    Go To  ${PREVIOUS SURVEYS URL}

Go To Logout Page
    Go To  ${LOGOUT URL}
