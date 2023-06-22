*** Settings ***
Resource  resource.robot
Documentation     Testing
Library    SeleniumLibrary
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
#Library    Browser


*** Variables ***
${DATA COUNT}    105
${TOY DATA COUNT TEST CASE 1}    18
# Note: it counts the header riw as 2 rows


*** Test Cases ***
Click 'Kokeile valmiilla datalla' link
    Go To Main Page
    Click Link     Kokeile valmiilla datalla
    Excel Page Should Be Open

Results page has table and table has content
    Wait Until Page Contains Element    //table
    Element Should Be Visible    //table
    ${Rows}=    get element count    xpath://table[@id='results_table']/tbody/tr
    Log To Console     ${Rows}
    Should Be Equal As Strings    ${DATA COUNT}   ${Rows} 

Excel Export button is present and functional
    Page Should Contain    Vie tulokset Excel-taulukkoon
    Click Element        //*[contains(text(),'Vie tulokset Excel-taulukkoon')]
    Title Should Be     Tulokset - Piryopt

Main Page 'Kokeile luoda dataa' link is functional
    Go To Main Page
    Click Link    Kokeile luoda dataa
    Toy Data Input Page Should Be Open

'Kokeile luoda dataa' form in functional
    Go To Toy Data Input Page 
    Title Should Be    Data input - Piryopt
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
    Click Element        //*[contains(text(),'Luo dataa!')] 

Toy data results are correct
    Title Should Be     Tulokset - Piryopt
    Page Should Contain     Lajittelun tulokset
    Page Should Contain     Ryhmänvalintojen keskiarvo
    Page Should Contain     1.0. valinta:
    Page Should Contain     aikaa kului
    Page Should Contain     Opiskelijat on lajiteltu ryhmiin seuraavasti   
    Page Should Contain    Vie tulokset Excel-taulukkoon
    Page Should Contain    Palaa etusivulle
    Wait Until Page Contains Element    //table
    Element Should Be Visible    //table
    ${Rows}=    get element count    xpath://table[@id='results_table']/tbody/tr
    Log To Console     ${Rows}
    Should Be Equal As Strings    ${TOY DATA COUNT TEST CASE 1}    ${Rows}
