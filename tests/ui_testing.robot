*** Settings ***
Documentation     Testing
Library    SeleniumLibrary
#Library    Browser


*** Variables ***
${BROWSER}    firefox
${MAIN_URL}    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/ 
${EXCEL URL}    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/excel
${TOY DATA FORM}    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/input 
${TOY DATA RESULTS URL}    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/results
${DATA COUNT}    105
${TOY DATA COUNT TEST CASE 1}    18
# Note: it counts the header riw as 2 rows


*** Test Cases ***
Open Browser To Main Page
    Open Browser    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/ 
    Title Should Be     Hello World - Piryopt
    Page Should Contain    Index
    Page Should Contain    Hello from flask!
    Page Should Contain    Kokeile luoda dataa
    Page Should Contain    Kokeile valmiilla datalla

Click 'Kokeile valmiilla datalla' link
    Click Link     Kokeile valmiilla datalla
    Location Should Be     ${EXCEL URL}
    Title Should Be     Tulokset - Piryopt

Results page has required texts
    Location Should Be     ${EXCEL URL}
    Title Should Be     Tulokset - Piryopt
    Page Should Contain     Lajittelun tulokset
    Page Should Contain     Ryhmänvalintojen keskiarvo
    Page Should Contain     1.0. valinta:
    Page Should Contain     2.0. valinta:
    Page Should Contain     3.0. valinta: 
    Page Should Contain     aikaa kului
    Page Should Contain     Opiskelijat on lajiteltu ryhmiin seuraavasti

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


Click 'Palaa etusivulle' link and close broser (end of testing)
    Click Link     Palaa etusivulle
    Location Should Be     ${MAIN URL}
    Title Should Be     Hello World - Piryopt
    close browser

Main Page 'Kokeile luoda dataa' link is functional
    Open Browser    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/ 
    Title Should Be     Hello World - Piryopt
    Click Link    Kokeile luoda dataa
    Location Should Be   ${TOY DATA FORM}
    close browser

'Kokeile luoda dataa' form in functional
    Open Browser    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/input 
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
    Location Should Be     ${TOY DATA RESULTS URL}
    Title Should Be     Tulokset - Piryopt
    Page Should Contain     Lajittelun tulokset
    Page Should Contain     Ryhmänvalintojen keskiarvo
    Page Should Contain     1.0. valinta:
    Page Should Contain     2.0. valinta:
    Page Should Contain     aikaa kului
    Page Should Contain     Opiskelijat on lajiteltu ryhmiin seuraavasti   
    Page Should Contain    Vie tulokset Excel-taulukkoon
    Page Should Contain    Palaa etusivulle
    Wait Until Page Contains Element    //table
    Element Should Be Visible    //table
    ${Rows}=    get element count    xpath://table[@id='results_table']/tbody/tr
    Log To Console     ${Rows}
    Should Be Equal As Strings    ${TOY DATA COUNT TEST CASE 1}    ${Rows} 
    close browser

