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