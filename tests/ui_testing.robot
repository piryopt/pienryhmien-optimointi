*** Settings ***
Documentation     Testing
Library    SeleniumLibrary
#Library    Browser


*** Variables ***
${BROWSER}    firefox
${MAIN_URL}    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/ 
${EXCEL URL}    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/excel 


*** Test Cases ***
Open Browser To Main Page
    Open Browser    https://piryopt.ext.ocp-test-0.k8s.it.helsinki.fi/ 
    Title Should Be     Hello World - Piryopt

Click 'Kokeile valmiilla datalla' link
    Click Link     Kokeile valmiilla datalla
    Location Should Be     ${EXCEL URL}
    Title Should Be     Tulokset - Piryopt

Results page has Results
    Location Should Be     ${EXCEL URL}
    Page Should Contain     Lajittelun tulokset
    Page Should Contain     Ryhmänvalintojen keskiarvo
    Page Should Contain     aikaa kului
    Page Should Contain     Opiskelijat on lajiteltu ryhmiin seuraavasti

*** Keywords ***