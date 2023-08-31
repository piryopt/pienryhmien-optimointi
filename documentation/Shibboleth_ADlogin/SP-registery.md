# Guide for the app's SP registry stuff
https://sp-registry.it.helsinki.fi/

You should have access to the registry based on your IAM group, but that wasn't the case for us. Atleast one of you should login, and if you don't have the access, contact the email in the error message to gain access.

## Overview
SP registry contains important functionalities for the AD login:
- define the Shibboleth attributes used by the app
- define important routes for AD login
- define certificates
- create AD login test users (test server only)

Details later

## Front page
The relevant parts here are the two links https://piryopt.ext.ocp-(test|prod)-0.k8s.it.helsinki.fi. The other two are something added by the university IT staff for their purposes.

Test and production servers have their own entityIDs and configurations etc. but they are mostly similar. The production version requires more information, but it's explained later.

IMPORTANT: making changes to the production version requires approval from the university registry admins (they are notified automatically), which may take some time, so test thoroughly in the test version first. The test version's changes don't need approval and come into effect in 15 minutes or something.

Clicking the link takes you to the next view.

## SP Configuration

### Summary
Summary of the later tabs' information

### Basic Information
Mostly self-explanatory, I don't think any of these need to be changed. Privacy policy URLs need to be changed if its place is changed.

### Technical Attributes
Probably better to not touch anything here. The entityID is set here, and if you get the jakaja(-test).it.helsinki.fi name change to work, the entityID need to be changed to it.

### Attributes
When a user logs into the app succesfully, the app gets information about the user, and the information it gets is defined here. You need to give a reason for using the attribute.

All attributes\
https://wiki.helsinki.fi/pages/viewpage.action?pageId=226580829


### Certificates
Certificates needed in OpenShift and in the next part are added here. When creating the keys with the ssl command, the address should be the entityID, and the -shib should be removed. When adding a certificate, use the .crt file and check both signing and encryption boxes. I don't think anything here needs to be changed.

### SAML Endpoints
These addresses make the AD login and logout work (I think). Nothing here probably needs to be changed. As you can see there are two versions, the piryopt.ext.ocp and jakaja.it versions. If you get the name change working, the logout/in addresses should be already set, but I'm not sure.

### Contacts
Production use requires someone working for the university as contact, they are defined here.

### Admins
I made our IAM group admins but they couldn't even log in, so nothing useful here (atleast for us)

### Test Users
(Test server only) Test users are created here. There are examples, they should be explanatory enough.