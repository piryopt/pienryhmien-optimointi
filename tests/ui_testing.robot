*** Settings ***
Resource  resource.robot
Documentation     Testing
Library    SeleniumLibrary
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
#Library    Browser


*** Variables ***
${DATA COUNT}    104
${TOY DATA COUNT TEST CASE 1}    17
${EXCELBUTTON}    xpath=//button[@type='submit' and contains(text(),'Vie tulokset Excel-taulukkoon')]
# Note: it counts the header riw as 2 rows


*** Test Cases ***

Excel Results page has table and table has content
    Go To Excel Page
    Wait Until Page Contains Element    //table
    Element Should Be Visible    //table
    ${Rows}=    get element count    xpath://table[@id='results_table']/tbody/tr
    Log To Console     ${Rows}
    Should Be Equal As Strings    ${DATA COUNT}   ${Rows}

'Kokeile luoda dataa' form in functional
    Go To Toy Data Input Page 
    Title Should Be    Data input - Jakaja
    Wait Until Element Is Visible    group_n
    Click Element    group_n
    Input Text        group_n    4
    Wait Until Element Is Visible    group_size
    Click Element    group_size
    Input Text        group_size    4
    Wait Until Element Is Visible    student_n
    Click Element    student_n
    Input Text        student_n    16
    Wait Until Element Is Visible    max_selections
    Click Element    max_selections
    Input Text        max_selections    2
    Click Button  inputbutton

Toy data results are correct
    Title Should Be     Tulokset - Jakaja
    Page Should Contain     Lajittelun tulokset
    Page Should Contain     Ryhmänvalintojen keskiarvo
    Page Should Contain     1. valintaansa sijoitetut opiskelijat:
    Page Should Contain     Opiskelijat on lajiteltu ryhmiin seuraavasti   
    Page Should Contain    Vie tulokset Excel-taulukkoon
    Wait Until Page Contains Element    //table
    Element Should Be Visible    //table
    ${Rows}=    get element count    xpath://table[@id='results_table']/tbody/tr
    Log To Console     ${Rows}
    Should Be Equal As Strings    ${TOY DATA COUNT TEST CASE 1}    ${Rows}
    Click Element  ${EXCELBUTTON}
    Title Should Be     Tulokset - Jakaja
