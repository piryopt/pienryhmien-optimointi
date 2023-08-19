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

${SURVEY 1 NAME}  Case all mandatory, yes rejecting choices
${SURVEY 2 NAME}  Case all mandatory, no rejecting choices
${SURVEY 3 NAME}  Case not all mandatory, yes rejecting choices
${SURVEY 4 NAME}  Case not all mandatory, no rejecting choices

${SURVEY 1 HREF}  xpath=//a[contains(text(), '${SURVEY 1 NAME}')]
${SURVEY 2 HREF}  xpath=//a[contains(text(), '${SURVEY 2 NAME}')]
${SURVEY 3 HREF}  xpath=//a[contains(text(), '${SURVEY 3 NAME}')]
${SURVEY 4 HREF}  xpath=//a[contains(text(), '${SURVEY 4 NAME}')]

${AD_LOGIN_BUTTON}    xpath=//button[@type='submit' and contains(text(),'Login')]
${FIRST_TIME_LOGIN_ACCEPT}  xpath=//button[@type='submit' and contains(text(),'Accept')]
${CREATE_NEW_SURVEY_BUTTON}  xpath=//button[@type='submit' and contains(text(),'Luo kysely')]

${SURVEY SUBMIT ANSWER}  xpath=//button[@type='submit' and contains(text(),'Lähetä valinnat')]

*** Test Cases ***
Create Secondary Teacher Account
    [Tags]  asd
    [Documentation]  You can't give access to account that doesn't exist, this is just for that
    Login And Go To Main Page  robottiTeacher2  moi123

Login As Teacher
    [Tags]  asd
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Login And Go To Main Page  robottiTeacher  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely


Create Survey As Teacher Case 1
    # Create case 1: all mandatory, yes rejecting choices
    Go To Create Survey Page
    Set Create Survey Time Fields  01.08.2023  01:01  01.08.2024  02:02
    Input Text  groupname  ${SURVEY 1 NAME}
    Set Focus To Element  denied-choices-count
    Input Text  denied-choices-count  1
    Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey2.csv
    Wait Until Page Contains Element  ${CREATE_NEW_SURVEY_BUTTON}
    Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    Click Element  ${CREATE_NEW_SURVEY_BUTTON}

    Go To  ${SURVEYS URL}
    Click Element  ${SURVEY 1 HREF}
    ${SURVEY 1 URL}=  Get Location
    Set Suite Variable  ${SURVEY 1 URL}


Test Survey Case 1
    Go To  ${SURVEY 1 URL}
    Page Should Contain  Case all mandatory, yes rejecting choices

    # drag more than allowed to reject box
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  id:sortable-bad
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Toivo')]  id:sortable-bad
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Floora')]  id:sortable-good
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]  id:sortable-good
    Input Text  id:reasons  ässitfarcenim äisimhi tunappat nelo
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Et voi hylätä näin montaa vaihtoehtoa

    # dragging one isn't enough
    Go To  ${SURVEY 1 URL}
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  id:sortable-bad
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Et ole tehnyt riittävän monta valintaa!

    # now all are dragged, but reason for rejecting is missing
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]  id:sortable-good
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Toivo')]  id:sortable-good
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Floora')]  id:sortable-good
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Perustelu on liian lyhyt, tallennus epäonnistui

    # giving the reason
    Input Text  id:reasons  ässitfarcenim äisimhi tunappat nelo
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Tallennus onnistui


Create Survey As Teacher Case 2

    # Create case 2: all mandatory, no rejecting choices
    Go To Create Survey Page
    Set Create Survey Time Fields  01.08.2023  01:01  01.08.2024  02:02
    Set Focus To Element  groupname
    Input Text  groupname  ${SURVEY 2 NAME}
    Click Element  id:min-choices-no
    Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey2.csv
    Wait Until Page Contains Element  ${CREATE_NEW_SURVEY_BUTTON}
    Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    Click Element  ${CREATE_NEW_SURVEY_BUTTON}

    Go To  ${SURVEYS URL}
    Click Element  ${SURVEY 2 HREF}
    ${SURVEY 2 URL}=  Get Location
    Set Suite Variable  ${SURVEY 2 URL}

Test Survey Case 2
    Go To  ${SURVEY 2 URL}
    Page Should Contain  Case all mandatory, no rejecting choices

    Page Should Not Contain Element  id:sortable-bad

    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]  id:sortable-good
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  id:sortable-good
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Et ole tehnyt riittävän monta valintaa!

    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Floora')]  id:sortable-good
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Toivo')]  id:sortable-good
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Tallennus onnistui

Create Survey As Teacher Case 3
    

    # Create case 3: not all mandatory, yes rejecting choices
    Go To Create Survey Page
    Set Create Survey Time Fields  01.08.2023  01:01  01.08.2024  02:02
    Set Focus To Element  groupname
    Input Text  groupname  ${SURVEY 3 NAME}
    Set Focus To Element  denied-choices-count
    Input Text  denied-choices-count  1
    Click Element  id:min-choices-custom
    Input Text  minchoices  2
    Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey2.csv
    Wait Until Page Contains Element  ${CREATE_NEW_SURVEY_BUTTON}
    Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    Click Element  ${CREATE_NEW_SURVEY_BUTTON}

    Go To  ${SURVEYS URL}
    Click Element  ${SURVEY 3 HREF}
    ${SURVEY 3 URL}=  Get Location
    Set Suite Variable  ${SURVEY 3 URL}

Test Survey Case 3
    
    Go To  ${SURVEY 3 URL}
    Page Should Contain  Case not all mandatory, yes rejecting choices

    # drag more than allowed to reject box
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  id:sortable-bad
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Toivo')]  id:sortable-bad
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Floora')]  id:sortable-good
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]  id:sortable-good
    Input Text  id:reasons  ässitfarcenim äisimhi tunappat nelo
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Et voi hylätä näin montaa vaihtoehtoa

    # minchoices is set to 2, one isn't enough
    Go To  ${SURVEY 3 URL}
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Floora')]  id:sortable-good
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Sinun pitää valita enemmän vaihtoehtoja

    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  id:sortable-good
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Tallennus onnistui
    

Create Survey As Teacher Case 4
    [Tags]  asd
    # Create case 4: not all mandatory, no rejecting choices
    Go To Create Survey Page
    Set Create Survey Time Fields  01.08.2023  01:01  01.08.2024  02:02
    Set Focus To Element  groupname
    Input Text  groupname  ${SURVEY 4 NAME}
    Click Element  id:min-choices-custom
    Input Text  minchoices  2
    Set Focus To Element  id:min-choices-no
    Click Element  id:min-choices-no
    Choose File  ${FILE_UPLOAD_BUTTON}  ${CURDIR}/test_files/test_survey2.csv
    Wait Until Page Contains Element  ${CREATE_NEW_SURVEY_BUTTON}
    Set Focus To Element  ${CREATE_NEW_SURVEY_BUTTON}
    Click Element  ${CREATE_NEW_SURVEY_BUTTON}

    Go To  ${SURVEYS URL}
    Click Element  ${SURVEY 4 HREF}
    ${SURVEY 4 URL}=  Get Location
    Set Suite Variable  ${SURVEY 4 URL}

Test Survey Case 4
    Go To  ${SURVEY 4 URL}
    Page Should Contain  Case not all mandatory, no rejecting choices
    Page Should Not Contain Element  id:sortable-bad

    # minchoices is set to 2, one isn't enough
    Go To  ${SURVEY 4 URL}
    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Floora')]  id:sortable-good
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Sinun pitää valita enemmän vaihtoehtoja

    Drag And Drop  xpath=//h5[contains(text(),'Päiväkoti Nalli')]  id:sortable-good
    Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    Click Button  ${SURVEY SUBMIT ANSWER}
    Page Should Contain  Tallennus onnistui

Test Survey Choice Search
    [Tags]  asd

    # Wait Until Page Contains Element  id:deleteSubmission
    # Set Focus To Element  id:deleteSubmission
    # Click Button  id:deleteSubmission

    # Wait Until Page Contains Element  id:confirmDelete
    # Set Focus To Element  id:confirmDelete
    # Click Button  id:confirmDelete

    Go To  ${SURVEY 4 URL}

    Input Text  id:searchChoices  00790
    
    # don't use Should Contain Element, all the elements exists, just hidden
    Element Should Be Visible  xpath=//h5[contains(text(),'Päiväkoti Toivo')]

    Element Should Not Be Visible  xpath=//h5[contains(text(),'Päiväkoti Nalli')]
    Element Should Not Be Visible  xpath=//h5[contains(text(),'Päiväkoti Kotikallio')]
    Element Should Not Be Visible  xpath=//h5[contains(text(),'Päiväkoti Floora')]

Give Another Teacher Rights
    [Tags]  asd
    Go To Survey Answers Page  ${SURVEY 4 URL}

    Input Text  id:teacher_email  robotti.2.teacher@helsinki.fi

    Click Button  addin_teacher_time

Login As Teacher Another Teacher
    [Tags]  asd
    [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
    Login And Go To Main Page  robottiTeacher2  moi123
    Page Should Contain  Näytä vanhat kyselyt
    Page Should Contain  Luo uusi kysely

    Page Should Contain  Case not all mandatory, no rejecting choices


# Login As Student
#     [Documentation]  Wait Until because AD login redirects, home url isn't opened instantly. Times out after 5s and fails if not opened
#     Login And Go To Main Page  robottiStudent  moi123
#     Page Should Contain  Näytä vanhat kyselyt
#     Page Should Not Contain  Luo uusi kysely

# Go To Create Survey Page As Student
#     Go To Create Survey Page
#     Page Should Contain  Näytä vanhat kyselyt
#     Page Should Not Contain  Luo uusi kysely

# Answer Survey As Student
#     [Documentation]  This test might fail if survey is already answered
#     Go To  ${SURVEY 1 URL}
#     Page Should Contain  Päiväkoti Toivo
#     Page Should Contain  Päiväkoti Nalli
#     Page Should Contain  Päiväkoti Floora
#     Page Should Contain  Päiväkoti Kotikallio
    

    # Wait Until Page Contains Element  ${SURVEY SUBMIT ANSWER}
    # Set Focus To Element  ${SURVEY SUBMIT ANSWER}
    # Click Button  ${SURVEY SUBMIT ANSWER}
    # Page Should Contain  Tallennus onnistui
