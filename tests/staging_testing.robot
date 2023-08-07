*** Settings ***
Documentation  Testing
Library  SeleniumLibrary
Suite Setup  Open And Configure Browser S
Suite Teardown  Close Browser

*** Variables ***
${SERVER}  piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/
${BROWSER}  headlessfirefox
${DELAY}  0.0 seconds
${HOME_URL}  https://${SERVER}
${LOGOUT URL}  http://${SERVER}/auth/logout

${AD_LOGIN_BUTTON}  xpath=//button[@type='submit' and contains(text(),'Login')]

*** Test Cases ***
Login As Teacher
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Go To Logout Page
    Go To Main Page
    Input Text  username  outi1
    Input Text  password  moi123
    Click Element  ${AD_LOGIN_BUTTON}
    Wait Until Location Is  ${HOME_URL}
    Go To Main Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely

Login As Student
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Go To Logout Page
    Go To Main Page
    Input Text  username  olli1
    Input Text  password  moi123
    Click Element  ${AD_LOGIN_BUTTON}
    Wait Until Location Is  ${HOME_URL}
    Go To Main Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely

*** Keywords ***
Go To Main Page
    Go To  ${HOME_URL}

Go To Logout Page
    Go To  ${LOGOUT URL}

Open And Configure Browser S
    Open Browser  browser=${BROWSER}
    Set Window Size  1920  1080
    Set Selenium Speed  ${DELAY}