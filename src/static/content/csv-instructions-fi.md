# Ohje kyselyn luomiseen CSV-tiedostosta

Kyselyn vaihtoehdot on mahdollista tuoda CSV-tiedostosta näitä ohjeita noudattamalla. CSV on lyhenne sanoista "Comma-Separated Values". CSV tiedostossa tieto on siis tallennettu siten, että sarakkeet on eroteltu jollain merkillä (tyypillisesti pilkulla).

Jakajassa CSV tiedoston erottajalla ei ole väliä (voi olla esimerkiksi , tai ;). Pakolliset tiedot jokaiselle kohtelle on nimi, paikkamäärä ja ryhmien minimikoko. Tiedoston ylimmän rivin tulee olla otsikkorivi eli vähintään seuraavanlainen: </br>
"Päiväkodin nimi", "Paikkamäärä", "Minimikoko"</br></br>

Alla oleva kuva näyttää esimerkkitiedoston muodon:
<img src="/static/images/csv.png" alt="Esimerkki csv-tiedosto">
</br></br>

Jakaja pudottaa oletuksena epäsuositun ryhmä-vaihtoehdon, jos sen minimikoko ei täyty jaossa. Jos haluat, että jotkut ryhmät
toteutuvat varmasti voit lisätä CSV tiedostoon sarakkeen "Mandatory" ja täyttää sen arvoilla TRUE tai FALSE sen mukaan onko ryhmä pakollinen vai ei. Sarakkeen "Mandatory" arvot voivat olla esimerkiksi TRUE, true tai True eli kirjainkoolla ei ole välilä. FALSE arvoa ei periaatteessa ole pakko antaa, muttaa sarake tarvitsee joka rivillä jonkin arvon (esimerkiksi tyhjät lainausmerkit " " käyvät hyvin). 

Alla oleva kuva näyttää esimerkkitiedoston muodon, jossa on sellaisia ryhmiä joiden on pakko toteutua:
<img src="/static/images/csv2.png" alt="Esimerkki csv-tiedosto">


## E-lomake
Luodessasi kyselyä E-lomakkeessa, sinun täytyy kysyä ensimmäisessä kentässä kohteen nimeä, toisena kohteen paikkamäärää (positiivinen kokonaisluku) ja kolmantena ryhmien minimikoko (positiivinen kokonaisluku), muuten kohteiden tuonti CSV-tiedostosta ei toimi. Vastausnäkymän pitäisi näyttää jotakuinkin tältä:

Kyselyn vastausnäkymä, johon päiväkoti yms. täyttää oman tietonsa
<img src="/static/images/csv-reply-view.png" alt="Vastausnäkymä käyttäjälle">

Kolmessa ensimmäisessä kohdassa nimellä ei ole väliä (Päiväkodin nimi, nimi, tunnus yms. tai paikkamäärä, enimmäispaikat yms. kaikki käyvät ja min_size, minimikoko jne.), kunhan järjestys on oikea. 

Ylläolevaan kyselyn vastaaminen tuottaa tälläisen CSV-tiedoston, joka löytyy Elomakkeen kohdasta lomakeraportti:
<img src="/static/images/csv-report-view.png" alt="Lomakeraportti">

<strong>Kaksi ensimmäistä saraketta ovat turhia (Tall.id, Tallennusaika), joten poista ne luodusta .csv tiedostosta.</strong> 
