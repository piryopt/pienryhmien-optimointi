# More practical explanation of Shibboleth/AD-login


## How the AD login works
When accessing the site, the user is redirected to the AD login page. Upon correct credentials, the Shibboleth server will redirect the user to the app, with the Shibboleth attributes in the headers, which are then read in the routes.py ad_login() decorator/middleware.

Which attributes are received is defined in SP registry, which has its own file.
## List of current attributes

| "technical" name     | actually is      | OID/Name                          | Example               |
|----------------------|------------------|-----------------------------------|-----------------------|
| cn                   | Name of user     | urn:oid:2.5.4.3                   | Aaro Esimerkki        |
| eduPersonAffiliation | List of roles    | urn:oid:1.3.6.1.4.1.5923.1.1.1.1  | member;student        |
| mail                 | University email | urn:oid:0.9.2342.19200300.100.1.3 | aaro.esim@helsinki.fi |

List of all attributes
https://wiki.helsinki.fi/pages/viewpage.action?pageId=226580829