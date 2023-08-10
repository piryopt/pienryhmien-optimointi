# Jakaja-sovelluksen käyttöohje opettajalle

## Yleiskatsaus sovellukseen
TODO


## 1. Sisäänkirjautuminen

Sovelluksen käyttämiseen tarvitseen Helsingin yliopiston käyttäjätunnukset. 


## 2. Käyttöoikeudet

Jakaja-sovellus tunnistaa kahdenlaisia käyttäjiä:
- opettaja
- oppilas

Sovellus tunnistaa käyttäjätason automaattisesti sisäänkirjautumisen yhteydessä. Opettaja-tason oikeudet saavat kaikki sellaiset käyttäjät, jotka kuuluvat Helsingin yliopiston opetushenkilökuntaan. Oppilaskäyttäjiä ovat kaikki muut HY-kirjautumista käyttävät henkilöt.


## 3. Uuden kyselyn luominen

Vain opettajakäyttäjä voi luoda uusia kyselyjä.

Kyselyn luominen alkaa etusivun "Luo uusi kysely" -nappia painamalla. Sovellus avaa lomakkeen, joka täytetään seuraavasti:

**1. Kyselyn nimi**
- Anna kyselylle selkeä, kuvaava nimi. Nimen tulee olla vähintään 5 merkkiä pitkä (sisältäen välilyönnit).
- Nimen tulee olla uniikki, joten jos kysely toistuu vuosittain, voi olla hyvä idea lisätä nimen perään lukuvuosi ja/tai periodi. 

**2. Vastausaika**
- Anna kyselylle alku- ja päättymisaika. Klikkaa ensimmäistä tyhjää kenttää ja valitse päivämäärä kalenterista tai kirjoita se muodossa pp.kk.vvvv. Aseta kellonaika muodossa hh:mm. Huom: kyselyn päättymisaika ei voi olla menneisyydessä.
- Sovellus sulkee kyselyn sen sulkeutumisaikana. Tarvittaessa voit avata kyselyn uudelleen (ks. kohta x).

**3. Kyselyn kuvaus**
- Kirjoita tähän kenttään lyhyt kuvaus kyselyn tarkoituksesta ja ohje käyttäjälle. Tämä kenttä ei ole pakollinen, mutta on suositeltavaa käyttää sitä.
- Kerro, onko opiskelijan asetettava kaikki vaihtoehtot mielekkyysjärjestykseen (vihreä laatikko), vai riittääkö esim. 5 vaihtoehtoa. 
- Kerro myös, jos opiskelijalla on mahdollisuus lisätä vaihtoehtoja ei-listalle (punainen laatikko), esimerkiksi jos hänellä on vaikka oma lapsi tietyssä päiväkodissa. Ei-listalle lisääminen vaatii aina perustelut ja tämä on hyvä mainita myös kuvauksessa.

**4. Priorisoitujen ryhmien vähimmäismäärä**
- Merkitse tähän kenttään lukumäärä sille, kuinka monta vaihtoehtoa opiskelijan tulee vähintään valita ja asettaa toivomusjärjestykseen. Luvun on oltava kokonaisluku.
- Joissakin kyselyissä voi olla tarpeen vaatia, että opiskelija asettaa kaikki kyselyn vaihtoehdot toivomusjärjestykseen. Siinä tapauksessa laita tähän kenttään luku, joka vastaa priorisoitavien ryhmien määrää.
- Jos vaihtoehtoja on valittavana paljon (20+), kuten esimerkiksi harjoituspaikkakyselyssä, on suositeltavaa antaa opiskelijalle sitä pienempi määrä, esimerkiksi 5 tai 10 valintaa. 

**5. Priorisoitavat ryhmät**
- Priorisoitavat ryhmät ovat vaihtoehtoja, joista opiskelijat voivat kertoa toiveensa, ja joihin sovellus jakaa heidät kyselyn päätyttyä. 
- Voit lisätä vaihtoehdot manuaalisesti käsin kirjoittamalla tai tuomalla ne suoraan csv-tiedostosta. 

**5.1 Ryhmien tuominen csv-tiedostosta**

TODO
- CSV on tiedostomuoto, jossa taulukkomuodossa oleva tieto on tallennettu tekstitiedostoksi niin, että eri solujen arvot on eroteltu pilkulla ([Wikipedia-linkki](https://fi.wikipedia.org/wiki/CSV))
linkki elomake-pohjaan
linkki elomakkeen yleiseen 
Mahdolliset ongelmatilanteet

**5.2. Ryhmien lisääminen käsin**
- Kirjoita nimi-kenttään vaihtoehdon nimi (esimerkiksi ryhmän aihe, harjoittelupäiväkodin nimi) ja enimmäispaikat-kenttään tieto siitä, kuinka monta opiskelijaa voidaan valita tähän vaihtoehtoon.
- "+ Lisää tietokenttä" -nappia painamalla voit lisätä vaihtoehdolle lisätietoja, esimerkiksi harjoittelupaikkakyselyssä tähän kenttään voi lisätä päiväkodin osoitteen, lapsiryhmän kuvauksen tai muuta oleellista tietoa. Kyselyä täyttäessään opiskelija näkee nämä lisätiedot kun klikkaa vaihtoehtoa. Lisätietokenttiä voi olla useita.
****

## Kyselyn sulkeminen
TODO

## Kyselyn avaaminen uudelleen
TODO

## Ryhmiin jakaminen
TODO

Perustilanne
Jos jakopaikkoja on vähemmän kuin kyselyyn vastanneita

## Kyselyn käyttöoikeuksien jakaminen toiselle opettajalle
TODO

## Kuinka jakoalgoritmi toimii
TODO (linkki?)

## Mahdolliset ongelmatilanteet
TODO
Kyselylinkki ei toimi
En ole tyytyväinen lajitteluun


## Tuki
TODO