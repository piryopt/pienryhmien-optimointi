*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Variables ***
${SERVER}  127.0.0.1:5000
${BROWSER}  firefox
${DELAY}  0.2 seconds
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
    Login And Go To Main Page  robottiTeacher  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely

Create Survey As Teacher From CSV
    Go To Create Survey Page
    Title Should Be  Luo uusi kysely - Jakaja
    Set Create Survey Mandatory Fields  ${SURVEY 1 NAME}  01.08.2023  01:01  01.08.2024  02:02  2
    Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey2.csv
    Wait Until Page Contains  Päiväkoti Floora
    Wait Until Page Contains Element  ${CREATE_NEW_SURVEY_BUTTON}
    Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    Click Element  ${CREATE_NEW_SURVEY_BUTTON}

    Go To  ${SURVEYS URL}
    Page Should Contain  ${SURVEY 1 NAME}
    Wait Until Page Contains Element  ${SURVEY HREF}
    Set Focus To Element  ${SURVEY HREF}
    Click Element  ${SURVEY HREF}

    Drag To Top Of Choices  xpath=//h5[contains(text(),'Päiväkoti Floora')]
    Drag To Top Of Choices  xpath=//h5[contains(text(),'Päiväkoti Nalli')]
    Drag To Top Of Choices  xpath=//h5[contains(text(),'Päiväkoti Toivo')]
    Drag To Top Of Choices  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]

    ${SURVEY 1 URL}=  Get Location
    Set Suite Variable  ${SURVEY 1 URL}

    Page Should Contain  Päiväkoti Toivo
    Page Should Contain  Päiväkoti Floora
    Page Should Contain  Päiväkoti Kotikallio
    Page Should Contain  Päiväkoti Nalli

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

    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]  id:sortable-bad
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Toivo')]  id:sortable-bad
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  id:sortable-bad
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Floora')]  id:sortable-bad
    # Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Enkeksi')]  id:sortable-bad
    # Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Gehenna')]  id:sortable-bad
    # Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti A')]  id:sortable-bad
    # Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti B')]  id:sortable-bad
    # Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti C')]  id:sortable-bad
    # Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti D')]  id:sortable-bad

    Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]  -300  0
    Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti Toivo')]  -300  0
    Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  -300  0
    Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti Floora')]  -300  0
    # Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti Enkeksi')]  0  -3000
    # Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti Gehenna')]  0  -3000
    # Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti A')]  0  -3000
    # Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti B')]  0  -3000
    # Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti C')]  0  -3000
    # Run Keyword And Ignore Error  Drag And Drop By Offset  xpath=//h5[contains(text(),'Päiväkoti D')]  0  -3000
    

    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Tallennus onnistui
