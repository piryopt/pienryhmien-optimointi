# University of Helsinki AD login ---> Haka login
This is a quick guide on how to change University of Helsinki (UH) AD login to Haka login. This guide will assume you already have a working UH AD login, and that SP registries aren't completely new to you etc. I'm not an expert on this subject, I'm just writing what I know.

This project's original AD login was built on a few guides and help from the university's people, and I don't know if there's other ways to do it, but this worked for us. Maybe it won't work for everyone, but if for example you're on the course Ohjelmistotuotantoprojekti and have followed those examples and guides, I think this will work.

This guide is valid as of when it was last updated, and probably won't be updated.
### Fun(?) fact
This implementation might actually be against Haka's rules, because [a guide](https://wiki.eduuni.fi/display/CSCHAKA/Request+for+tender+templates) says : "The service must support the use of local user accounts. The capability must be available concurrently with Haka." I'm not sure what 'local account' means in this context, [the Finnish version](https://wiki.eduuni.fi/pages/viewpage.action?pageId=27297797) is "Järjestelmään tulee voida kirjautua myös suoraan ilman Haka-kirjautumista. Ominaisuuden tulee olla käytettävissä samanaikaisesti Haka-kirjautumisen rinnalla." Maybe it means that you should be able to register with email, or that you should keep the home organization's login, but the point is that this implementation  has neither. You've been warned.

### Quick overview of our deployment
This app is deployed to the university's OpenShift, running two pods: the application itself, and the Shibboleth pod, that's built on two images, tike/openshift-sp-httpd and tike/openshift-sp-shibd. I'm pretty sure that the Shibboleth pod is set up as a reverse proxy. It's assumed that your setup is like this also.

### Limitation
Implementing Haka login this way will direct the user directly to the Haka login page, in contrast to using Moodle, where clicking the login button on the front page will direct you to choose which login (UH AD, Haka, EDUgain) you want to use. This guide will not help you do that.

## Haka Resource Registry (cf. UH SP registry)
Let's first submit the SP application(s) to Haka's version of UH SP registry, the [Resource Registry](https://rr.funet.fi/rr/spmenu.php). Click Add a new Service Provider to start. Both production and testing versions will be explained.

###  Organization Information
In `select organization` choose Helsingin yliopisto, rest of the fields should fill themselves. I didn't put anything into `PartnerForm ID`

### SP Basic Information
`Service Provider Information` should be self-explanatory, I left `Service Login Page URL` empty.

`Discovery Response URL #1` for us it was `<entity id>/Shibboleth.sso/Login`. [Guide (in Finnish) how to find it](https://wiki.eduuni.fi/display/CSCHAKA/Discovery+Response)

Check both boxes `urn:oasis:names:tc:SAML:2.0:nameid-format:transient` and `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent` (cf. SP registry Technical Attributes). `Subject Identifier` as Not in use.
According to [this guide](https://wiki.eduuni.fi/pages/viewpage.action?pageId=27297748) there should be an option to choose something other than Haka test, but I didn't have that. In the testing version I checked the Haka test box. In prodction I left it unchecked, and when the email notifiying that the application had been accepted, I replied to that email and requested for it to be put into production.

### SP SAML Endpoints
This is pretty much the same as SP registry, just copy those from there.

### Certificates
Copy the site's certificate for example from OpenShift without the ---BEGIN--- and ---END--- lines.

### The rest
The rest should be self-explanatory. Didn't change anything in `UI Extensions`

### After submitting
After the Haka people have accepted your application you'll get an email. According to [this guide](https://wiki.eduuni.fi/display/CSCHAKA/Testipalvelimet) you should get test credentials with the test version, but I didn't get them and had to ask for them.

It reads [here](https://wiki.eduuni.fi/display/CSCHAKA/Metadata) that the metadata is updated usually on Wednesdays. I **think** you know it's updated when you open `haka-metadata.xml` on that page and you can find your site's entity ID etc. there. That site also has lots of important information, such as how to select the correct organization in testing.

## Shibboleth configuration
Great news: you (or atleast we had to) have to edit only three lines in one file to get this working. The edited file is the Shibboleth configuration file, which is called `shib_config` if you followed the 'Ohtuprojekti' guide. I don't know the official names for these things, so bear with me.

Change these lines:

### Test
`<SSO entityID="https://login-test.it.helsinki.fi/shibboleth">SAML2</SSO>`\
to\
`<SSO discoveryProtocol="SAMLDS" discoveryURL="https://testsp.funet.fi/DS">SAML2</SSO>`

`url="https://login-test.it.helsinki.fi/metadata/sign-hy-test-metadata.xml"`\
to\
`url="https://haka.funet.fi/metadata/haka_test_metadata_signed.xml"`

[Test certificate](https://wiki.eduuni.fi/display/CSCHAKA/Testipalvelimet), download `haka_testi_2018_sha2.crt` and save it somewhere where Shibboleth can find it, we have it as a OpenShift secret.\
`<MetadataFilter type="Signature" certificate="sign-login.helsinki.fi.crt"/>`\
to\
`<MetadataFilter type="Signature" certificate="/shib-certs/haka_testi_2018_sha2.crt"/>`

### Production
`<SSO entityID="https://login.helsinki.fi/shibboleth">SAML2</SSO>`\
to\
`<SSO discoveryProtocol="SAMLDS" discoveryURL="https://haka.funet.fi/DS">SAML2</SSO>`

`url="https://login.helsinki.fi/metadata/sign-hy-metadata.xml"`\
to\
`url="https://haka.funet.fi/metadata/haka-metadata-v9.xml"`

[Production certificate](https://wiki.eduuni.fi/display/CSCHAKA/Metadata), download `haka-sign-v9.pem`, and same as above. The version numbers seems to change occasionally, so it might not be v9 when you see this.\
`<MetadataFilter type="Signature" certificate="sign-login.helsinki.fi.crt"/>`\
to\
`<MetadataFilter type="Signature" certificate="/shib-certs/haka-sign-v9.pem"/>`

## Closing thoughts
After all the steps have been taken and the Shibboleth pod/server restarted, everything should work.

Maybe I forgot to mention something, but this should get you quite far.
