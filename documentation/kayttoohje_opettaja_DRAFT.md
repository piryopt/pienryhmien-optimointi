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

Kirjaudu sovellukseen osoitteessa [jakaja.it.helsinki.fi](jakaja.it.helsinki.fi) Helsingin yliopiston käyttäjätunnuksillasi.

<kbd>
<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/kirjautumissivu.png" width="70%" height="70%">
</kbd>

[lisätietoa käyttätunnuksista](https://helpdesk.it.helsinki.fi/kirjautuminen-ja-yhteydet/kayttajatunnus/kayttajatunnukset).


## 2. Käyttöoikeudet

Jakaja-sovelluksessa on kahdenlaisia käyttäjiä:
- opettaja
- opiskelija

Sovellus tunnistaa käyttäjätason automaattisesti sisäänkirjautumisen yhteydessä. Opettaja-tason oikeudet saavat kaikki sellaiset käyttäjät, jotka kuuluvat Helsingin yliopiston opetushenkilökuntaan. Kaikki muut käyttäjät ovat opiskelijakäyttäjiä.

Opettajakäyttäjän oikeuksiin kuuluu:
- uuden kyselyn luominen 
- oman kyselyn muokkaaminen
- kyselyn sulkeminen
- lajittelutoiminto (ryhmiin jakaminen)
- yksittäisten vastausten poistaminen kyselystä (esim. jos joku peruu osallistumisensa kurssille)
- kyselyn kopioiminen pohjaksi uudelle kyselylle
- kyselyn oikeuksien jakaminen toiselle opettajalle

Opettajan etusivu näyttää tältä:

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/etusivu.png" width="70%" height="70%">

Toimintopainikkeet:
- Luo uusi kysely
- Näytä vanhat kyselyt

Niiden alla näkyy listana omat, käynnissä olevat kyselyt.



## 3. Uuden kyselyn luominen

Vain opettajakäyttäjä voi luoda uusia kyselyjä.

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/luo_kysely.png" width="70%" height="70%">

Kyselyn luominen alkaa etusivun "Luo uusi kysely" -nappia painamalla. Sovellus avaa lomakkeen, joka täytetään seuraavasti:

**3.1. Kyselyn nimi**

- Anna kyselylle selkeä, kuvaava nimi. Nimen tulee olla vähintään 5 merkkiä pitkä (sisältäen välilyönnit).
- Nimen tulee olla uniikki, joten jos kysely toistuu vuosittain, voi olla hyvä idea lisätä nimen perään lukuvuosi ja/tai opetusperiodi. 


**3.2. Vastausaika**

- Anna kyselylle alku- ja päättymisaika. Klikkaa kenttää ja valitse päivämäärä kalenterista tai kirjoita se muodossa pp.kk.vvvv. Aseta kellonaika muodossa hh:mm.
- Sovellus ehdottaa alkamisajaksi kuluvaa päivää ja asettaa sen valmiiksi, mutta voit halutessasi muuttaa sitä.
- **Huom:** kyselyn päättymisaika ei voi olla menneisyydessä.
- Sovellus sulkee kyselyn sen sulkeutumisaikana. Tarvittaessa voit avata kyselyn uudelleen (ks. kohta 6.).

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/pvm_asetus.png" width="70%" height="70%">


<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/kellonaika.png" width="60%" height="60%">


**3.3. Kyselyn kuvaus**

- Kirjoita tähän kenttään lyhyt kuvaus kyselyn tarkoituksesta ja ohje käyttäjälle. Tämä kenttä ei ole pakollinen, mutta sitä on suositeltavaa käyttää.
- Kerro, onko opiskelijan asetettava kaikki vaihtoehtot mielekkyysjärjestykseen (vihreä laatikko), vai riittääkö esim. 5 vaihtoehtoa. 
- Kerro myös, jos opiskelijalla on mahdollisuus lisätä vaihtoehtoja ei-listalle (punainen laatikko, ks. kohta 3.5 valintojen kieltämisestä), jolloin häntä ei jostakin painavasta syystä voi sijoittaa näihin ryhmiin. Ei-listalle lisääminen vaatii aina perustelun vastaajalta ja tämä on hyvä mainita myös kuvauksessa.


**3.4. Vaaditaanko kaikkien ryhmien järjestämistä?**

- Valitse "kyllä", jos haluat, että opiskelijan on asetettava kaikki kyselyn vaihtoehdot toivejärjestykseensä. 
- Valitse "ei", jos riittää, että opiskelija laittaa järjestykseen vain osan vaihtoehdoista. Tässä tapauksessa avautuu uusi kenttä "Priorisoitujen ryhmien vähimmäismäärä", johon sinun tulee määritellä kokonaislukuna tuo vähimmäismäärä. Jos opiskelija valitsee liian vähän vaihtoehtoja, sovellus huomauttaa siitä:

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/vastauslomake_liian_vahan_valintoja.png" width="60%" height="60%">


- Jos vaihtoehtoja on valittavana paljon (20+), kuten esimerkiksi harjoituspaikkakyselyssä, on suositeltavaa antaa opiskelijalle koko määrää pienempi määrä, esimerkiksi 5 tai 10 valintaa. 
- **HUOM** Ryhmäjaon onnistumisen kannalta on tärkeää saada kyselyn vastaajilta riittävästi tietoa ryhmien kiinnostavuudesta. Jos pakollisia valintoja on esimerkiksi vain yksi, algoritmi suosii jonkin verran vain yhden paikan valinneita kun heitä verrataan kaikki valinnat kiinnostusjärjestykseen laittaneisiin. Kannattaa vaatia vähintään 3-5 paikan järjestämistä riippuen vaihtoehtojen lukumäärästä.


**3.5. Sallitaanko valintojen kieltäminen?**

- Joissakin kyselyissä on perustultua antaa opiskelijan kertoa, jos jokin kyselyn vaihtoehdoista ei ollenkaan sovi hänelle. Valitse kyllä, jos haluat sallia tämän. Kun opiskelija käyttää tätä mahdollisuutta kyselyyn vastatessaan, perustelut-kenttä kyselylomakkeella muuttuu pakolliseksi ja näet perustelut yhteenvedosta. 
- Sovellus huomauttaa opiskelijalle, jos perustelut puuttuvat:

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/vastauslomake_perustelu.png" width="60%" height="60%">


**3.6. Näytetäänkö vastaajalle hakupalkki?**

- Hakupalkin avulla kyselyyn vastaaja voi etsiä vastausvaihtoehtoja nimen tai vastausvaihtoehdon lisätietojen perusteella
- Hakupalkki kannattaa näyttää kun vaihtoehtoja on paljon, mutta sen voi halutessaan piilottaa, esimerkiksi jos kyselyssä on vähän vaihtoehtoja jotka pitää kaikki järjestää

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/vastauslomake_.haku.png" width="70%" height="70%">


**3.7. Priorisoitavat ryhmät**

- Priorisoitavat ryhmät ovat vaihtoehtoja, joista opiskelijat voivat kertoa toiveensa, ja joihin sovellus jakaa heidät kyselyn päätyttyä. 
- Voit lisätä vaihtoehdot manuaalisesti käsin kirjoittamalla tai tuomalla ne suoraan csv-tiedostosta. Opiskelijan avatessa lomakkeen vaihtoehdot näkyvät seuraavasti:

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/vastauslomake_tyhja.png" width="70%" height="70%">


- Vaihtoehdoille voi lisätä lisätietoja, jotka tulevat vastaajale näkyviin vaihtoehtoa klikatessa:

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/vastauslomake_lisatieto.png" width="70%" height="70%">


**3.7.1 Ryhmien tuominen csv-tiedostosta**

- CSV on tiedostomuoto, jossa taulukkomuodossa oleva tieto on tallennettu tekstitiedostoksi niin, että eri solujen arvot on eroteltu pilkulla. ([Lisätietoa Wikipediassa](https://fi.wikipedia.org/wiki/CSV)). 

linkki elomake-pohjaan (TBA)
[linkki elomakkeen yleiseen ohjeeseen](https://helpdesk.it.helsinki.fi/help/11144)
Mahdolliset ongelmatilanteet (TBA)

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/csv.png" width="70%" height="70%">


**3.7.2. Ryhmien lisääminen käsin**

- Kirjoita nimi-kenttään vaihtoehdon nimi (esim. ryhmän aihe, harjoittelupäiväkodin nimi) ja enimmäispaikat-kenttään tieto siitä, kuinka monta opiskelijaa voidaan valita tähän vaihtoehtoon.
- "+ Lisää tietokenttä" -nappia painamalla voit lisätä vaihtoehdolle lisätietoja, esimerkiksi harjoittelupaikkakyselyssä tähän kenttään voi lisätä päiväkodin osoitteen, lapsiryhmän kuvauksen tai muuta oleellista tietoa. Kyselyä täyttäessään opiskelija näkee nämä lisätiedot kun klikkaa vaihtoehtoa. Lisätietokenttiä voi olla useita.

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/lisatietokentta.png" width="70%" height="70%">


**3.8 Luo kysely**

- Klikatessasi kyselyn luomisnappia saat alapalkkiin tiedon kyselyn luomisen onnistumisesta tai täydennystarpeesta
- Kun kysely on luotu, jää sivu edelleen kyselyn luomiseen. Jos täydennät tai muokkaat kyselyyn annettuja tietoja ja painat uudelleen "Luo kysely" nappia luodaan uusi kysely päivitetyillä tiedoilla

## 4. Valmiin kyselylomakkeen tarkastelu ja opiskelijoille lähetettävän linkin kopiointi

- Kun olet luonut kyselyn, se ilmestyy "Näytä vanhat kyselyt" listaukseen, johon on linkki etusivulla. Mikäli kyselyn vastausaika on alkanut, se näkyy sinulle myös Jakajan etusivulla "Käynnissä olevat kyselyt" otsikon alla
- Mene "Näytä vanhat kyselyt"-listaukseen ja klikkaa kyselyn nimeä, jolloin sinulle avautuu kyselyn vastaussivu
- Kopioimalla selaimen osoiterivin saat linkin, jolla voit jakaa kyselyn
- Voit tällä sivulla myös kokeilla kyselyyn vastaamista


## 5. Kyselyn sulkeminen

- Klikkaa kyselyn nimeä etusivun listasta otsikon "Käynnissä olevat kyselyt" alta tai "Aiemmat kyselyt" listauksesta kyselyn kohdalta "Tarkastele tuloksia" linkkiä. Näet yhteenvedon kyselyn vastaustilanteesta.
- Sulje kysely klikkaamalla sivun oikeassa reunassa olevaa "Sulje kysely" -nappia. Sovellus varmistaa valinnan kysymällä "Haluatko varmasti sulkea kyselyn?". Klikkaa pop-up-ikkunasta vaihtoehtoa "OK".

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/kyselyn_sulku_popup.png" width="60%" height="60%">
</kbd>

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/suljettu_kysely.png" width="70%" height="70%">


- Kysely on nyt suljettu eikä siihen voi syöttää uusia vastauksia. Jos haluat avata kyselyn uudelleen, katso tämän ohjeen kohta 6. Jos haluat jakaa kyselyyn vastanneet opiskelijat ryhmiin käyttäen sovelluksen lajittelualgoritmia, katso kohta 8.


## 6. Suljetun kyselyn avaaminen uudelleen

- Klikkaa "Aiemmat kyselyt" listauksesta kyselyn kohdalta "Tarkastele tuloksia" linkkiä. Näet yhteenvedon kyselyn vastaustilanteesta.
- Avaa kysely uudestaan klikkaamalla sivun oikeassa reunassa näkyvää keltaista "Avaa kysely uudestaan"-nappia. Sovellus varmistaa valinnan kysymällä "Haluatko varmasti avata kyselyn?". Klikkaa pop-up-ikkunasta vaihtoehtoa "OK".
- Kysely on nyt auki ja siihen voi vastata.


## 7. Kyselyn muokkaaminen

- Kyselyn muokkaukseen pääset "Aiemmat kyselyt" listauksesta klikkaamalla kyselyn kohdalla "Muokkaa kyselyä" 
- Voit muokata esimerkiksi kyselyn nimeä, kyselyn kuvausta ja vastausaikaa

**7.1 Kyselyn käyttöoikeuksien jakaminen toiselle opettajalle**

- Muokkauslomakkeen alussa voit lisätä toiselle opettajalle oikeudet kyselyyn kirjoittamalla hänen helsinki.fi sähköpostiosoitteensa kenttään ja painamalla "Lisää opettaja"-nappia
- Tällöin lisätyllä opettajalla on yhtäläiset oikeudet kyselyyn kuin sinulla. Hän voi esimerkiksi muokata kyselyä, tarkastella sen tuloksia, sulkea kyselyn ja tehdä ryhmäjaon.


**7.2 Kyselyn vastausvaihtoehtojen muokkaaminen**

- Kyselyn vastausvaihtoehtoja ei voi tällä hetkellä muokata
- Kyselyn voi kopioida uudeksi kyselyksi, jolloin vaihtoehtojen vapaa muokkaaminen on mahdollista (ks. kohta 9.), mutta tällöin menetetään kaikki kyselyssä jo mahdollisesti olevat vastaukset
- Kyselyssä olemassaolevien vaihtoehtojen paikkamäärää voi muokata mikäli paikkoja on vähemmän kuin kyselyssä vastauksia (ks. kohta 8.1)


## 8. Ryhmiin jakaminen ja tulosten käsittely

- Siirry kyselyn yhteenvetosivulle sovelluksen etusivulta klikkaamalla ensin "Näytä vanhat kyselyt" -nappia ja valitse sitten haluamasi kysely klikkaamalla kyselyn kohdalla olevaa "Tarkastele tuloksia" -linkkiä.
- Jos kyselyä ei ole vielä suljettu, tee se ensin (ks. kohta 5). Kyselyn sulkeuduttua kyselyn yhteenvetosivulle ilmestyy sininen nappi "Jaa ryhmiin". Mikäli kyselyssä ei ole enemmän vastauksia kuin paikkoja, voit suorittaa ryhmiin jaon suoraan.

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/vastaukset_ennen_lajittelua.png" width="70%" height="70%">

- Sivun yläreunassa lukee kyselyn nimi ja sen alla näet vastausten määrän sekä jaettavien paikkojen määrän. Jos vastauksia on enemmän kuin paikkoja,sovellus varoittaa siitä. Siinä tapauksessa sinun on tehtävä muutoksia ennen kuin voit tehdä ryhmiin jakamisen (ks. kohta 8.1).


- Tarkista ensin vastaukset. Jos siellä on mukana ylimääräisiä vastauksia, esimerkiksi sellaisilta opiskelijoilta, jotka ovat peruneet kurssille osallistumisensa, voit poistaa nuo vastaukset klikkaamalla vastauksen kohdalla olevaa nappia "Poista tämä vastaus". 

**8.1 Ryhmäkokojen muokkaus**

- Jos vastauksia on enemmän kuin paikkoja, ohjeistaa sovellus muokkaamaan ryhmäkokoja ylimääräisten vastausten poiston jälkeen
- Klikkaa ohjeistuksen alla olevaa "Muokkaa ryhmäkokoja"-nappia, jolloin pääset ryhmäkokojen muokkaukseen


<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/ryhmakoon_muutos.png" width="70%" height="70%">

- Sivulla näet yläkulmassa vastausten ja paikkojen kokonaismäärän, sekä ryhmät
- Ryhmien kohdalla näet sekä paikkamäärän että ryhmän suosittuuden, suosittuus kertoo kuinka moni on sijoittanut kyseisen ryhmän top 3 vaihtoehtoihinsa
- Ryhmäkokoja muokatessa älä muokkaa ryhmän nimeä tai muokkaus ei tallennu
- Mikäli ylimääräiset vastaajat on mahdollista sijoittaa ryhmiin lisäämällä ryhmäkokoja, on se kannattava vaihtoehto
- Jos on tarve luoda kokonaan uusi ryhmä, katso ohjeistus kohdasta 8.2 ja varmista, että ylimääräiseen ryhmään jää riittävästi opiskelijoita. Jos siis ylimääräisten vastausten määrä on pienempi kuin haluttu ryhmäkoko, kannattaa vähentää olemassaolevissa ryhmissä ryhmäkokoa niin, että yli jäävien opiskelijoiden määrä on sopiva. Tällöin uuteen ryhmään sijoitetut opiskelijat valitaan algoritmilla mahdollisimman reilusti


**8.2 Ryhmiin jako kun vastauksia on liikaa**

- Jos vastauksia on edelleen liikaa ylimääräisten vastausten poistamisen ja ryhmäkokojen muokkaamisen jälkeen, voit silti jakaa opiskelijat ryhmiin
- Tällöin kyselyyn luodaan ryhmä "Tyhjä", jossa on yhtä monta paikkaa kuin ylimääräisiä vastauksia
- Kyselyyn vastanneet sijoitetaan toivoidensa mukaan ryhmiin sillä erotuksella, että nyt osa jää ryhmien ulkopuolelle ja näkyvät ryhmässä "Tyhjä" ryhmäjaon tuloksia tarkasteltaessa


**8.3 Tulosten käsittely**

- Kun ryhmäjako on tehty painamalla nappia "Jaa ryhmiin", voit tallentaa tehdyn ryhmäjaon painamalla nappia "Tallenna tulokset", jolloin ryhmäjako tallentuu sovellukseen. Muuten poistuessasi sivulta unohtaa sovellus tehdyn ryhmäjaon ja voit jakaa opiskelijat uudelleen ryhmiin.

<img src="https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/Pictures/lajittelun_jalkeen_lista.png" width="70%" height="70%">

- Tuloksessa voi olla ryhmäjakokertojen välillä eroa mikäli kovin monella opiskelijalla on samat valinnat kyselyssä, sillä ryhmäjakoa tehdessä opiskelijoiden järjestys satunnaistetaan ja algoritmi suosii listassa ensimmäisenä olevaa henkilöä joilla on samat valinnat.
- Kun ryhmäjaon tulokset on tallennettu _et voi enää avata kyselyä uudestaan_ mutta sitä voi käyttää pohjana uudelle kyselylle
- Ryhmäjaon tulokset voi tallentaa Excel-taulukkoon klikkaamalla "Vie tulokset Excel-taulukkoon"-nappia


## 9. Kyselyn kopiointi uudeksi kyselyksi

- Mene "Aiemmat kyselyt listaukseen"
- Valitse haluamasi kyselyn riviltä "Kopioi kysely"-linkki
- Avautuu kyselynluontipohja, jossa on esisyötettynä vanhan kyselyn tiedot
- Voit päivittää kaikkia kyselyyn liittyviä kenttiä samoin kuin uuden kyselyn luonnissa (ks. kohta 3. uuden kyselyn luominen)
- Mikäli kopioimasi kysely on edelleen käynnissä, täytyy kopioidulla kyselyllä olla eri nimi ennen kuin sen voi tallentaa


## 10. Mahdolliset ongelmatilanteet

**Kyselylinkki ei toimi**

Onhan kyselylomake varmasti avoinna? Tarkista, että kyselyä ei ole suljettu manuaalisesti, ja että kyselyn sulkeutumisajankohta on tulevaisuudessa. Tarkista myös, että opiskelijoille jakamasi linkki viittaa haluamaasi lomakkeeseen.


**Kyselylomakkeeseen vastaaminen ei onnistu**

Jos opiskelija ei pysty tallentamaan vastausta, syynä voi olla jokin seuraavista:
- Opiskelija on valinnut vähemmän vaihtoehtoja kuin mitä on asetettu vähimmäismääräksi
- Opiskelija on valinnut jotakin punaiseen ei-ruutuun, mutta ei ole täyttänyt perustelut-kenttää tai kentässä oleva vastaus on liian lyhyt
- HY-kirjautuminen on vanhentunut


**Kyselylomaketta luodessa sen tallentaminen ei onnistu**

Tarkista:
- Onhan kyselyn jokaiselle vaihtoehdolle määritelty vähimmäismäärä, joka on kokonaisluku ja suurempi kuin 0?


## 10. Tuki

TBA