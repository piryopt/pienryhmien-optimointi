# Ohje kyselyn luomiseen CSV-tiedostosta

Sovelluksessa on mahdollista tuoda valittavat vaihtoehdot Elomake CSV-tiedostosta, kunhan luotu kysely noudattaa näitä tiettyjä ohjeita

## TÄRKEIN OSA

Luodessasi kyselyä Elomakkeessa, sinun täytyy kysyä ensimmäisessä kentässä kohteen nimeä ja toisena kohteen paikkamäärää (positiivinen kokonaisluku), muuten kohteiden tuonti CSV-tiedostosta ei toimi. Vastausnäkymän pitäisi näyttää jotakuinkin tältä:

Kyselyn vastausnäkymä, johon päiväkoti yms. täyttää oman tietonsa
![Kyselyn vastausnäkymä](/src/static/images/csv-reply-view.png)

Kahdessa ensimmäisessä kohdassa nimellä ei ole väliä (Päiväkodin nimi, nimi, tunnus yms. tai paikkamäärä, enimmäispaikat yms. kaikki käyvät), kunhan järjestys on oikea. 



Ylläolevaan kyselyn vastaaminen tuottaa tälläisen CSV-tiedoston, joka löytyy Elomakkeen kohdasta lomakeraportti:
![Lomakeraportti](/src/static/images/csv-report-view.png)

Kaksi ensimmäistä saraketta ovat turhia, mutta älä silti poista niitä, vaan voit käyttää CSV-tiedostoa sellaisenaan. Sovelluksen toteutuksessa kaksi ensimmäistä saraketta ohitetaan, joka tarkoittaa sitä, että muista palveluista (esim. Google Forms) tuodut CSVt eivät välttämättä toimi, jos ne eivät noudata samaa muotoa kuin Elomakkeen CSVt.

## Muuta

Ainoat pakolliset kentät ovat kohteen nimi ja paikkamäärä. Ensimmäisessä esimerkkikuvassa on kaksi lisätietokenttää, mutta voit lisätä niitä lomakkeeseen haluamasi määrän, kunhan muistat laittaa nimen ja paikkamäärän ensimmäiseksi.