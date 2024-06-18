# Ohje kyselyn luomiseen CSV-tiedostosta

Sovelluksessa on mahdollista tuoda valittavat vaihtoehdot CSV-tiedostosta, kunhan luotu kysely noudattaa näitä tiettyjä ohjeita

## TÄRKEIN OSA
Luodessasi kyselyä Elomakkeessa, sinun täytyy kysyä ensimmäisessä kentässä kohteen nimeä, toisena kohteen paikkamäärää (positiivinen kokonaisluku) ja kolmantena ryhmien minimikoko (positiivinen kokonaisluku), muuten kohteiden tuonti CSV-tiedostosta ei toimi. Vastausnäkymän pitäisi näyttää jotakuinkin tältä:

Kyselyn vastausnäkymä, johon päiväkoti yms. täyttää oman tietonsa
<img src="/static/images/csv-reply-view.png" alt="Vastausnäkymä käyttäjälle">

Kolmessa ensimmäisessä kohdassa nimellä ei ole väliä (Päiväkodin nimi, nimi, tunnus yms. tai paikkamäärä, enimmäispaikat yms. kaikki käyvät ja min_size, minimikoko jne.), kunhan järjestys on oikea. 

Ylläolevaan kyselyn vastaaminen tuottaa tälläisen CSV-tiedoston, joka löytyy Elomakkeen kohdasta lomakeraportti:
<img src="/static/images/csv-report-view.png" alt="Lomakeraportti">

<strong>Kaksi ensimmäistä saraketta ovat turhia (Tall.id, Tallennusaika), joten poista ne luodusta .csv tiedostosta.</strong> 

## Muuta
Ainoat pakolliset kentät ovat kohteen nimi, paikkamäärä ja ryhmien minimikoko. .csv tiedoston erottajalla ei ole väliä (voi olla , tai ; tai "," tms.), sillä Jakaja muuttaa ne automaattisesti ;. Alla oleva kuva näyttää esimerkkitiedoston muodon:
<img src="/static/images/csv.png" alt="Esimerkki csv-tiedosto">