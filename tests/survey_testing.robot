*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${SERVER}  127.0.0.1:5000
${BROWSER}  headlessfirefox
${DELAY}  0.0 seconds
${HOME_URL}  http://${SERVER}/
${LOGOUT URL}  http://${SERVER}/auth/logout
${CREATE SURVEY URL}  http://${SERVER}/surveys/create
${SURVEYS URL}  http://${SERVER}/surveys

${FILE_UPLOAD_BUTTON}  css=[type='file']

${SURVEY 1 NAME}  Robot created survey

${AD_LOGIN_BUTTON}    xpath=//button[@type='submit' and contains(text(),'Login')]
${FIRST_TIME_LOGIN_ACCEPT}  xpath=//button[@type='submit' and contains(text(),'Accept')]
${CREATE_NEW_SURVEY_BUTTON}  xpath=//button[@type='submit' and contains(text(),'Luo kysely')]

${SURVEY HREF}  xpath=//a[contains(text(), '${SURVEY 1 NAME}')]
${SURVEY SUBMIT ANSWER}  xpath=//button[@type='submit' and contains(text(),'Lähetä valinnat')]

*** Test Cases ***
Login As Teacher
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    [Tags]  temp
    Login And Go To Main Page  robottiTeacher  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely

Create Survey As Teacher From CSV
    [Tags]  temp
    # Go To Create Survey Page
    # Title Should Be  Luo uusi kysely - Jakaja
    # Set Create Survey Mandatory Fields  ${SURVEY 1 NAME}  01.08.2023  01:01  01.08.2024  02:02  2
    # Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey2.csv
    # Wait Until Page Contains  Päiväkoti Floora
    # Wait Until Page Contains Element  ${CREATE_NEW_SURVEY_BUTTON}
    # Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    # Click Element  ${CREATE_NEW_SURVEY_BUTTON}

    Go To  ${SURVEYS URL}
    Page Should Contain  ${SURVEY 1 NAME}
    Wait Until Page Contains Element  ${SURVEY HREF}
    Set Focus To Element  ${SURVEY HREF}
    Click Element  ${SURVEY HREF}

    ${green box}=  Get Vertical Position  id:sortable-good

    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti Floora')]  ${green box}
    Capture Page Screenshot
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  ${green box}
    Capture Page Screenshot
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti Toivo')]  ${green box}
    Capture Page Screenshot
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]  ${green box}
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti D')]  ${green box}
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti C')]  ${green box}
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti B')]  ${green box}
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti A')]  ${green box}
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti Enkeksi')]  ${green box}
    ${green box}=  Drag To Green Box Bottom  xpath=//h5[contains(text(),'Päiväkoti Gehenna')]  ${green box}

    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Tallennus onnistui

    ${SURVEY 1 URL}=  Get Location
    Set Suite Variable  ${SURVEY 1 URL}
    Go To  ${SURVEY 1 URL}

    Element Should Contain  css=#sortable-good > li:nth-child(1)  Päiväkoti Floora
    Element Should Contain  css=#sortable-good > li:nth-child(2)  Päiväkoti Nalli
    Element Should Contain  css=#sortable-good > li:nth-child(3)  Päiväkoti Toivo
    Element Should Contain  css=#sortable-good > li:nth-child(4)  Päiväkoti Kotikallio
    Element Should Contain  css=#sortable-good > li:nth-child(5)  Päiväkoti D
    Element Should Contain  css=#sortable-good > li:nth-child(6)  Päiväkoti C
    Element Should Contain  css=#sortable-good > li:nth-child(7)  Päiväkoti B
    Element Should Contain  css=#sortable-good > li:nth-child(8)  Päiväkoti A
    Element Should Contain  css=#sortable-good > li:nth-child(9)  Päiväkoti Enkeksi
    Element Should Contain  css=#sortable-good > li:nth-child(10)  Päiväkoti Gehenna

    Wait Until Page Contains Element  id:deleteSubmission
    Set Focus To Element  id:deleteSubmission
    Click Button  id:deleteSubmission

    Wait Until Page Contains Element  id:confirmDelete
    Set Focus To Element  id:confirmDelete
    Click Button  id:confirmDelete


Login As Student
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Login And Go To Main Page  robottiStudent  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely

Go To Create Survey Page As Student
    Go To Create Survey Page
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Not Contain  Luo uusi kysely

Answer Survey As Student
    [Documentation]  This test might fail if survey is already answered
    Go To  ${SURVEY 1 URL}
    Page Should Contain  Päiväkoti Toivo
    Page Should Contain  Päiväkoti Nalli
    Page Should Contain  Päiväkoti Floora
    Page Should Contain  Päiväkoti Kotikallio
    

    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Tallennus onnistui
