# Jakaja-sovelluksen käyttöohje opettajalle

## Sisällys
1. Sisäänkirjautuminen
2. Käyttöoikeudet
3. Uuden kyselyn luominen
6. Kyselyn sulkeminen
7. Kyselyn muokkaaminen
8. Ryhmiin jakaminen ja tulosten käsittely
9. Kyselyn käyttöoikeuksien jakaminen toiselle opettajalle
10. Kuinka lajittelu algoritmi toimii
11. Mahdolliset ongelmatilanteet
12. Tuki


## 1. Sisäänkirjautuminen

Kirjaudu sovellukseen osoitteessa [jakaja.it.helsinki.fi](jakaja.it.helsinki.fi)Helsingin yliopiston käyttäjätunnuksillasi [lisätietoa käyttätunnuksista](https://helpdesk.it.helsinki.fi/kirjautuminen-ja-yhteydet/kayttajatunnus/kayttajatunnukset).


## 2. Käyttöoikeudet

Jakaja-sovelluksessa on kahdenlaisia käyttäjiä:
- opettaja
- oppilas

Sovellus tunnistaa käyttäjätason automaattisesti sisäänkirjautumisen yhteydessä. Opettaja-tason oikeudet saavat kaikki sellaiset käyttäjät, jotka kuuluvat Helsingin yliopiston opetushenkilökuntaan. Kaikki muut käyttäjät ovat opiskelijakäyttäjiä.

Opettajakäyttäjän oikeuksiin kuuluu:
- uuden kyselyn luominen 
- oman kyselyn muokkaaminen
- kyselyn sulkeminen
- lajittelutoiminto (ryhmiin jakaminen)
- yksittäisten vastausten poistaminen kyselystä (esim. jos joku peruu osallistumisensa kurssille)
- kyselyn kopioiminen pohjaksi uudelle kyselylle
- kyselyn oikeuksien jakaminen toiselle opettajalle


## 3. Uuden kyselyn luominen

Vain opettajakäyttäjä voi luoda uusia kyselyjä.

Kyselyn luominen alkaa etusivun "Luo uusi kysely" -nappia painamalla. Sovellus avaa lomakkeen, joka täytetään seuraavasti:

**1. Kyselyn nimi**
- Anna kyselylle selkeä, kuvaava nimi. Nimen tulee olla vähintään 5 merkkiä pitkä (sisältäen välilyönnit).
- Nimen tulee olla uniikki, joten jos kysely toistuu vuosittain, voi olla hyvä idea lisätä nimen perään lukuvuosi ja/tai opetusperiodi. 

**2. Vastausaika**
- Anna kyselylle alku- ja päättymisaika. Sovellus ehdottaa alkamisajaksi kuluvaa päivää ja asettaa sen valmiiksi, mutta voit halutessasi muuttaa sitä. Klikkaa kenttää ja valitse päivämäärä kalenterista tai kirjoita se muodossa pp.kk.vvvv. Aseta kellonaika muodossa hh:mm. Huom: kyselyn päättymisaika ei voi olla menneisyydessä.
- Sovellus sulkee kyselyn sen sulkeutumisaikana. Tarvittaessa voit avata kyselyn uudelleen (ks. kohta x).

**3. Kyselyn kuvaus**
- Kirjoita tähän kenttään lyhyt kuvaus kyselyn tarkoituksesta ja ohje käyttäjälle. Tämä kenttä ei ole pakollinen, mutta on suositeltavaa käyttää sitä.
- Kerro, onko opiskelijan asetettava kaikki vaihtoehtot mielekkyysjärjestykseen (vihreä laatikko), vai riittääkö esim. 5 vaihtoehtoa. 
- Kerro myös, jos opiskelijalla on mahdollisuus lisätä vaihtoehtoja ei-listalle (punainen laatikko), esimerkiksi jos hänellä on vaikka oma lapsi tietyssä päiväkodissa. Ei-listalle lisääminen vaatii aina perustelut ja tämä on hyvä mainita myös kuvauksessa.

**4. Vaaditaanko kaikkien ryhmien järjestämistä?**
- Valitse "kyllä", jos haluat, että opiskelijan on asetettava kaikki kyselyn vaihtoehdot toivejärjestykseensä. 
- Valitse "ei", jos riittää, että opiskelija laittaa järjestykseen vain osan vaihtoehdoista. Tässä tapauksessa avautuu uusi kenttä " Priorisoitujen ryhmien vähimmäismäärä", johon sinun tulee määritellä kokonaislukuna tuo vähimmäismäärä. 
- Jos vaihtoehtoja on valittavana paljon (20+), kuten esimerkiksi harjoituspaikkakyselyssä, on suositeltavaa antaa opiskelijalle koko määrää pienempi määrä, esimerkiksi 5 tai 10 valintaa. 

**5. Sallitaanko valintojen kieltäminen?**
- Joissakin kyselyissä on perustultua antaa opiskelijan kertoa, jos jokin kyselyn vaihtoehdoista ei ollenkaan sovi hänelle. Valitse kyllä, jos haluat sallia tämän. Kun opiskelija käyttää tätä mahdollisuutta kyselyyn vastatessaan, perustelut-kenttä kyselylomakkeella muuttuu pakolliseksi ja näet perustelut yhteenvedosta.

**6. Priorisoitavat ryhmät**
- Priorisoitavat ryhmät ovat vaihtoehtoja, joista opiskelijat voivat kertoa toiveensa, ja joihin sovellus jakaa heidät kyselyn päätyttyä. 
- Voit lisätä vaihtoehdot manuaalisesti käsin kirjoittamalla tai tuomalla ne suoraan csv-tiedostosta. 

**6.1 Ryhmien tuominen csv-tiedostosta**

TODO
- CSV on tiedostomuoto, jossa taulukkomuodossa oleva tieto on tallennettu tekstitiedostoksi niin, että eri solujen arvot on eroteltu pilkulla ([Wikipedia-linkki](https://fi.wikipedia.org/wiki/CSV)). 

linkki elomake-pohjaan (TBA)
[linkki elomakkeen yleiseen ohjeeseen](https://helpdesk.it.helsinki.fi/help/11144)
Mahdolliset ongelmatilanteet (TBA)

**6.2. Ryhmien lisääminen käsin**
- Kirjoita nimi-kenttään vaihtoehdon nimi (esim. ryhmän aihe, harjoittelupäiväkodin nimi) ja enimmäispaikat-kenttään tieto siitä, kuinka monta opiskelijaa voidaan valita tähän vaihtoehtoon.
- "+ Lisää tietokenttä" -nappia painamalla voit lisätä vaihtoehdolle lisätietoja, esimerkiksi harjoittelupaikkakyselyssä tähän kenttään voi lisätä päiväkodin osoitteen, lapsiryhmän kuvauksen tai muuta oleellista tietoa. Kyselyä täyttäessään opiskelija näkee nämä lisätiedot kun klikkaa vaihtoehtoa. Lisätietokenttiä voi olla useita.

**Valmiin kyselylomakkeen tarkastelu ja opiskelijoille lähetettävän linkin kopiointi**

TODO


## 7. Kyselyn sulkeminen

Klikkaa kyselyn nimeä etusivun listasta otsikon "Käynnissä olevat kyselyt" alta. Näet yhteenvedon kyselyn vastaustilanteesta. Sulje kysely klikkaamalla sivun oikeassa reunassa olevaa "Sulje kysely" -nappia. Sovellus varmistaa valinnan kysymällä "Haluatko varmasti sulkea kyselyn?". Klikkaa pop-up-ikkunasta vaihtoehtoa "OK".

Kysely on nyt suljettu eikä siihen voi syöttää uusia vastauksia. Jos haluat avata kyselyn uudelleen, katso tämän ohjeen kohta 7.2. Jos haluat jakaa kyselyyn vastanneet opiskelijat ryhmiin käyttäen sovelluksen lajittelualgoritmia, katso kohta 8.


## 8. Kyselyn muokkaaminen
TODO

**8.1. Auki olevan kyselyn muokkaaminen**

**8.2. Suljetun kyselyn avaaminen uudelleen ja lomakkeen muokkaaminen**


## 9. Ryhmiin jakaminen ja tulosten käsittely


Siirry kyselyn yhteenvetosivulle sovelluksen etusivulta klikkaamalla ensin "Näytä vanhat kyselyt" -nappia ja valitse sitten haluamasi kysely klikkaamalla kyselyn kohdalla olevaa "Tarkastele tuloksia" -linkkiä.

Jos kyselyä ei ole vielä suljettu, tee se ensin (ks. kohta 6). Kyselyn sulkeuduttua kyselyn yhteenvetosivulle ilmestyy sininen nappi "Jaa ryhmiin". 

Sivun yläreunassa lukee kyselyn nimi ja sen alla näet vastausten määrän sekä jaettavien paikkojen määrän. Jos vastauksia on enemmän kuin paikkoja,sovellus varoittaa siitä. Siinä tapauksessa sinun on tehtävä muutoksia ennen kuin voit tehdä ryhmiin jakamisen.

Tarkista ensin vastaukset. Jos siellä on mukana vastauksia sellaisilta opiskelijoilta, jotka ovat peruneet kurssille osallistumisensa, voit poistaa nuo vastaukset klikkaamalla vastauksen kohdalla olevaa nappia "Poista tämä vastaus". 

**Ylimääräisten paikkojen lisääminen ryhmiin - TBA**


## 10. Kyselyn käyttöoikeuksien jakaminen toiselle opettajalle

Kyselyn yhteenvetosivulla on vihreä nappi "Lisää opettaja". Syötä sen yläpuolella olevaan tekstikenttään toisen opettajan HY-sähköpostiosoite ja klikkaa nappia. Oikeudet on nyt jaettu ja sovellukseen kirjautuessaan kollegasi näkee kyselyn vanhojen kyselyjen listassaan. Hän ei saa tästä erikseen ilmoitusta, joten voi olla hyvä idea lähettää hänelle sähköposti asiasta.


## 11. Mahdolliset ongelmatilanteet

**Kyselylinkki ei toimi**
Onhan kyselylomake varmasti avoinna? Tarkista, että kyselyä ei ole suljettu manuaaliseksi ja että kyselyn sulkeutumisajankohta on tulevaisuudessa.

**Kyselylomakkeeseen vastaaminen ei onnistu**
Jos opiskelija ei pysty tallentamaan vastausta, syynä voi olla jokin seuraavista:
- Opiskelija on valinnut vähemmän vaihtoehtoja kuin mitä on asetettu vähimmäismääräksi
- Opiskelija on valinnut jotakin punaiseen ei-ruutuun, mutta ei ole täyttänyt perustelut-kenttää tai kentässä oleva vastaus on liian lyhyt
- HY-kirjautuminen on vanhentunut

**Kyselylomaketta luodessa sen tallentaminen ei onnistu**
Tarkista seuraavat:
- Onhan kyselyn jokaiselle vaihtoehdolle määritelty vähimmäismäärä, joka on kokonaisluku ja suurempi kuin 0?


## 13. Tuki

TODO