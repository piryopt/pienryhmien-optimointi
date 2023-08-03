*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser

*** Test Cases ***
Open Main Page As Student Test
    Go To Main Page
    Go To Main Page
    Page Should Contain  Olli Opiskelija