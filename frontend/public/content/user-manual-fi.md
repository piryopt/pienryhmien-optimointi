# Käyttöohje

1. Kyselyn luominen
2. Monivaihisen kyselyn luominen
3. Kyselyn hallinta
4. Vastausten käsittely
5. Kyselyyn vastaaminen
6. Monivaiheiseen kyselyyn vastaaminen

Jakajan toiminnalisuudet näkyvät etusivulla seuraavasti:

<img src="images/front_page.png" alt="Front page" class="md-image" />

## 1. Kyselyn luominen

Kyselyn luominen alkaa etusivun "Luo uusi kysely"-nappia painamalla. Sovellus avaa lomakkeen, joka täytetään seuraavasti:

##### 1.1 Kyselyn nimi

- Anna kyselylle selkeä, kuvaava nimi. Nimen tulee olla vähintään 5 merkkiä pitkä.
- Nimen täytyy myös olla uniikki, koska Jakajassa ei voi olla samaan aikaan käynnissä montaa samannimistä kyselyä.

##### 1.2 Vastausaika

- Anna kyselylle alku- ja päättymisaika. Klikkaa kenttää ja valitse päivämäärä kalenterista tai kirjoita se muodossa pp.kk.vvvv. Aseta kellonaika muodossa hh:mm.
- **Huom:** kyselyn päättymisaika ei voi olla menneisyydessä.
- Sovellus sulkee kyselyn sen sulkeutumisaikana. Tarvittaessa voit avata kyselyn uudelleen (ks. kohta 3.3).

<img src="images/date_of_closing.png" alt="Date of closing" class="md-image" />

##### 1.3 Kyselyn kuvaus

- Kuvaus ei ole pakollinen. Tähän kenttää voit kuitenkin kirjoittaa lyhyen kuvauksen kyselystä tai antaa mahdollisia lisäohjeita vastaajille.

<img src="images/description.png" alt="Survey description" class="md-image" />

##### 1.4 Vaaditaanko kaikkien ryhmien järjestämitä?

- Valitse "kyllä", jos haluat, että opiskelijan on asetettava kaikki kyselyn vaihtoehdot toivejärjestykseensä.
- Valitse "ei", jos riittää, että opiskelija laittaa järjestykseen vain osan vaihtoehdoista. Tällöin avautuu uusi kenttä "Priorisoitujen ryhmien vähimmäismäärä", johon voit määritellä vähimmäismäärä kokonaislukuna:

<img src="images/number_of_prioritized_groups.png" alt="Minimum prioritized groups" class="md-image" />

- Järjestettävien vaihtoehtojen määrän rajoittaminen on suositeltavaa etenkin silloin, kun vaihtoehtoja on paljon (20+)
  - **HUOM** Ryhmäjaon onnistumisen kannalta on tärkeää saada kyselyn vastaajilta riittävästi tietoa ryhmien kiinnostavuudesta, joten älä aseta priorisoitavien ryhmien määrä liian pieneksi. On suositeltavaa vaatia vähintään 3-5 paikan järjestämistä riippuen vaihtoehtojen lukumäärästä.

##### 1.5 Sallitaanko valintojen kieltäminen

- Vastaa tähän kohtaan "kyllä", jos haluat antaa vastaajille mahdollisuuden kieltää joitan vaihtoehtoja. Tällöin avautuu uusi kenttä "Sallittu kiellettyjen ryhmien määrä", johon voit määrittää sallittujen kieltojen määrän kokonaislukuna
- Vastaajilta vaaditaan kieltämiseen vähintään 10 merkkiä pitä perustelu, jotka näet vastauksien yhteenvedossa:

<img src="images/allow_denied_choices.png" alt="Denied choices" class="md-image" />

##### 1.6 Prioriorisoitavat ryhmät

- Voit lisätä vaihtoehdot manuaalisesti käsin kirjoittamalla tai tuomalla ne suoraan csv-tiedostosta.
- Priorisoitavat ryhmät ovat vaihtoehtoja, joista opiskelijat voivat kertoa toiveensa, ja joihin sovellus jakaa heidät kyselyn päätyttyä.
- Jokaiselta vaihtoehdoilta vaaditaan vähintää seuraavat tiedot:
  - Nimi
  - Enimmäispaikat
  - Minimikoko (Jos ryhmän minimikoolla ei ole väliä, syötä 0.)
- Alle minimikoon jäävät ryhmät jätetään pois jaosta. Jos haluat, että tietty ryhmä toteutuu varmasti, rastita ryhmän vasemmalla puolella oleva **"Pakota minimikokoon"** laatikko.
- Lisäksi voit määrittää haluamiasi lisätietoja painamalla "+ Lisää tietokenttä" painiketta
  - Jos, et halua, että lisätietokentän tiedot näytetään vastaajille, laita sen tunnisteen perään tähti \*
  - Lisätietokentän voi poistaa painamalla sen yläpuolella olevaa roskakoria

Alla olevassa esimerkissä lisätietona on annettu postinumero ja osoite:

<img src="images/survey_choices.png" alt="Survey choices" class="md-image" />

Opiskelijan avatessa lomakkeen vaihtoehdot näkyvät seuraavasti:

<img src="images/answer_page.png" alt="Answer page" class="md-image" />

##### Vaihtoehtojen tuominen csv-tiedostosta

- csv on tiedostomuoto, jossa taulukkomuodossa oleva tieto on tallennettu tekstitiedostoksi niin, että eri solujen arvot on eroteltu pilkulla. ([Lisätietoa Wikipediassa](https://fi.wikipedia.org/wiki/CSV)).
- Tarkemmat ohjeet vaihtoehtojen tuomiseen csv-tiedostosta löytyy täältä: [csv-ohje](csv-instructions)

### Luo kysely

Kun vähintään kaikki pakolliset kohdat on täytetty voit luoda kyselyn painamalla vihreää "Luo kysely"-nappia lomakkeen lopussa. Jos kyselyn luominen epäonnistuu, sovellus antaa virheviestin, jossa kerrotaan mahdollisista täydennystarpeista.

- Kun olet luonut kyselyn, se ilmestyy sivulle "Näytä vanhat kyselyt". Sivulle pääse etusivula olevan napin kautta.
- Kysely näkyy myös etusivulla "Käynnissä olevat kyselyt" otsikon alla

---

## 2. Monivaiheisen kyselyn luominen

Monivaiheisen kyselyn luominen alkaa etusivun "Luo uusi kysely"-nappia painamalla. Sovellus avaa lomakkeen, jonka useimmat kohdat täytetään samaan tapaan kuin tavallisessa kyselyssä.
Lomakkessa on kuitenkin lisäksi lomakkeessa on seuraavat lisäkohdat:

#### 2.1 Sallitaanko poissaolot?

- Vastaa tähän kohtaan "kyllä", jos haluat, että vastaajat voivat merkitä itsensä poissaolevaksi.
  - Poissaolot sallitaan tällöin kaikissa vaiheissa

#### 2.2 Rajoita osallistumiskertoja

- Jos haluat rajoittaa kuinka monta kertaa vastaaja voi osallistua johonkin ryhmään, vastaa tähän kyllä.
  - Tämä tarkoittaa siis sitä, että jos vastaaja esimerkiksi ensimmäisesäs vaiheessa on sijoitettu ryhmään jonka osallistumiskertojen raja on 1, häntä ei enää myöhemmissä vaiheissa sijoiteta ryhmään.
- Enimmäisosallistumiskertojen määrän voit myöhemmin asettaa jokaiselle ryhmälle vaiheen priorisoitavien ryhmien taulukossa sarakkessaa "Osallistumiskerrat\*":

<img src="images/participation_limit.png" alt="Participation limit" class="md-image" />

- Jotta osallistumiskertojen rajoittaminen toimii oikein, tulee ryhmällä olla sama nimi kaikissa vaiheissa.

### 2.3 Vaiheiden hallinta

##### 2.3.1 Vaiheen lisääminen

- Voit lisätä kyselyyn vaiheita painamalla sinistä "Lisää vaihe"-nappia. Tällöin lomakkeeseen ilmestyy uusi taulukku, johon voit määrittää kyseisen vaiheen vaihtoehdot:

<img src="images/stage.png" alt="Stage" class="md-image" />

##### 2.3.2 Vaiheen tunniste

- Jokaiselle vaiheelle tulee antaa uniikki tunniste.
  - Tunniste voi olla esimerkiksi vaiheen päivämäärä tai viikko.
- Vastaaja navigoi tunnisteiden avulla vaiheiden välillä, joten on suositeltavaa, että tunniste kuvaa selkeästi vaihetta.

##### 2.3.3 Vaihtoehtojen lisääminen vaiheeseen

- Vaihtoehtojen lisääminen vaiheisiin toimii samalla tavalla kuin tavallisessa kyselyssä. Voit lisätä vaihtoehdot manuaalisesti käsin kirjoittamalla tai tuomalla ne suoraan csv-tiedostosta.

##### 2.3.4 Vaiheen kopiointi

- Voit kopioida vaiheen painamalla sinistä "Kopioi vaihe" nappia. Tällöin kaikki vaiheen vaihtoehdot ja annetut tiedot kopioidaan uudeksi vaiheeksi

##### 2.3.5 Vaiheen poistaminen

- Voit poistaa vaiheen painamalla punaista "poista vaihe" nappia

---

## 3. Kyselyn hallinta

Kaikki tekemäsi kyselyt näkyvät "Näytä vanhat kyselyt"-sivulla, jonne pääset etusivulta nappia painamalla. Kyslyn hallintatoiminnallisuudet tuleva näkyviin painamalla kohtaa "Näytä":

<img src="images/survey_management.png" alt="Survey management" class="md-image" />

### 3.1 Kyselyn lähettäminen vastaajille

- Mene "Näytä vanhat kyselyt"-sivulle. Sivulle on linkki Jakajan etusivulla. Etsi listasta haluamasi kysely ja klikkaa kohtaa " Kopioi kyselyn osoite leikepöydälle"
- Vaihtoehtoisesti voit klikata kyselyn nimeä, jolloin sinulle avautuu kyselyn vastaussivu. Tällöin voit kopioida kyselyn osoitteen selaimen osoiterivin.
  - Voit myös halutessasi kokeilla kyselyynn vastaamista.

### 3.2 Kyselyn sulkeminen

- Klikkaa kyselyn nimeä etusivun listasta otsikon "Käynnissä olevat kyselyt" alta tai "Aiemmat kyselyt" listauksesta kyselyn kohdalta "Tarkastele tuloksia" linkkiä. Näet yhteenvedon kyselyn vastaustilanteesta.
- Sulje kysely klikkaamalla sivun oikeassa reunassa olevaa "Sulje kysely" -nappia.

### 3.3 Suljetun kyselyn avaaminen uudelleen

- Klikkaa "Aiemmat kyselyt" listauksesta kyselyn kohdalta "Tarkastele tuloksia" linkkiä. Näet yhteenvedon kyselyn vastaustilanteesta.
- Avaa kysely uudestaan klikkaamalla sivun oikeassa reunassa näkyvää keltaista "Avaa kysely uudestaan"-nappia. Sovellus varmistaa valinnan kysymällä "Haluatko varmasti avata kyselyn?". Klikkaa pop-up-ikkunasta vaihtoehtoa "OK".
- Kysely on nyt auki ja siihen voi vastata.

### 3.4 Hallintaoikeuksien antaminen toiselle käyttäjälle

- Hallintaoikeuksien lisääminen onnistuu muokkaus-sivulla.
  - Kyselyn muokkaukseen pääset "Näytä vanhat kyselyt" sivulta klikkaamalla kyselyn kohdalla linkkiä "Muokkaa kyselyä"
- Muokkauslomakkeen alussa voit lisätä toiselle opettajalle oikeudet kyselyyn kirjoittamalla hänen sähköpostiosoitteensa kenttään ja painamalla "Lisää opettaja"-nappia
  - Tällöin lisätyllä opettajalla on yhtäläiset oikeudet kyselyyn kuin sinulla. Hän voi esimerkiksi muokata kyselyä, tarkastella sen tuloksia, sulkea kyselyn ja tehdä ryhmäjaon.

<img src="images/admin.png" alt="Admin rights" class="md-image" />

### 3.5 Kyselyn muokkaaminen

- Kyselyn muokkaukseen pääset "Näytä vanhat kyselyt" sivulta klikkaamalla kyselyn kohdalla linkkiä "Muokkaa kyselyä".
- Muokkaussivulla näytetään kaikki kyselyn tiedot, mutta voit muokata vain kyselyn nimeä, kuvausta ja vastausaikaa.
- Voit muokata ryhmäkokoja vain silloin, kun kyselyyn vastanneita on enemmän kuin paikkoja (ks. kohta 4, Ryhmäjako, kun vastauksia on enemmän kuin paikkoja)

### 3.6 Kyselyn poistaminen

- Kyselyn voi poistaa Näytä vanhat kyselyt" sivulta klikkaamalla kohtaa "Poista kyselyt". Tällöin kysely siirretään roskakoriin.
- Roskakorista kysely poistuu pysysvästi automaattisesti viikon kouluttua. Jos haluat poistaa kyselyn välittömästi, etsi se roskakorista ja paina jälleen kohtaa "Poista kysely"

### 3.7 Kyselyn palauttaminen

- Poistetun kyselyn voi palauttaa roskakorista klikkaamlla "Palauta kysely" kohtaa.

### 3.8 Kyselyn kopioiminen

- Mene "Aiemmat kyselyt listaukseen"
- Valitse haluamasi kyselyn riviltä "Kopioi kysely"-linkki
- Avautuu kyselynluontipohja, jossa on esisyötettynä vanhan kyselyn tiedot
- Voit päivittää kaikkia kyselyyn liittyviä kenttiä samoin kuin uuden kyselyn luonnissa.
- Mikäli kopioimasi kysely on edelleen käynnissä, täytyy kopioidulla kyselyllä olla eri nimi ennen kuin sen voi tallentaa

## 4. Vastausten käsittely

#### 4.1 Vastauksien tarkastelu

- Pääset tarkastelemaan kyselyn vastauksia, menemällä "Näytä vanhat kyselyt" sivulle ja klikkaamalla kyselyn kohdalla " Tarkastele tuloksia".

#### 4.2 Ryhmäjako

- Siirry kyselyn yhteenvetosivulle sovelluksen etusivulta klikkaamalla ensin "Näytä vanhat kyselyt" -nappia ja valitse sitten haluamasi kysely klikkaamalla kohtaa "Tarkastele tuloksia".
- Jos kyselyä ei ole vielä suljettu, tee se ensin painamalla "Sulje kysely"-nappia
- Kun kysely on suljetty, yhteenvetosivulle ilmestyy sininen nappi "Jaa ryhmiin", jota painamalla voit suorittaa ryhmäjaon. -**HUOM!** Ennen ryhmäjaon tekemistä on suositeltavaa ensin tarkastaa vastaukset. Jos vastauksissa on mukana ylimääräisiä vastauksia (esimerkiksi opiskelijoilta, jotka ovat peruneet kurssille osallistumisensa), voit poistaa kyseiset vastaukset klikkaamalla vastauksen kohdalla olevaa nappia "Poista tämä vastaus".

#### 4.3 Ryhmäjako, kun vastauksia on enemmän kuin paikkoja

- Jos vastauksia on enemmän kuin paikkoja, ohjeistaa sovellus muokkaamaan ryhmäkokoja.
- Pääset muokkaamaan ryhmäkokoja painamalla "Muokkaa ryhmäkokoja"-nappia
- Sivulla näet yläkulmassa vastausten ja paikkojen kokonaismäärän, sekä ryhmät
- Ryhmien kohdalla näet sekä paikkamäärän että ryhmän suosittuuden, suosittuus kertoo kuinka moni on sijoittanut kyseisen ryhmän top 3 vaihtoehtoihinsa
- Ryhmäkokoja muokatessa älä muokkaa ryhmän nimeä tai muokkaus ei tallennu
- Mikäli ylimääräiset vastaajat on mahdollista sijoittaa ryhmiin lisäämällä ryhmäkokoja, on se kannattava vaihtoehto
- Jos vastauksia on edelleen liikaa ylimääräisten vastausten poistamisen ja ryhmäkokojen muokkaamisen jälkeen, voit silti jakaa opiskelijat ryhmiin
- Tällöin kyselyyn luodaan ryhmä "Tyhjä", jossa on yhtä monta paikkaa kuin ylimääräisiä vastauksia
- Kyselyyn vastanneet sijoitetaan toivoidensa mukaan ryhmiin sillä erotuksella, että nyt osa jää ryhmien ulkopuolelle ja näkyvät ryhmässä "Tyhjä" ryhmäjaon tuloksia tarkasteltaessa

#### 4.4 Tulosten käsittely

- Kun ryhmäjako on tehty painamalla nappia "Jaa ryhmiin", voit tallentaa tehdyn ryhmäjaon painamalla nappia "Tallenna tulokset", jolloin ryhmäjako tallentuu sovellukseen. Muuten poistuessasi sivulta unohtaa sovellus tehdyn ryhmäjaon ja voit jakaa opiskelijat uudelleen ryhmiin.
- Tuloksessa voi olla ryhmäjakokertojen välillä eroa mikäli kovin monella opiskelijalla on samat valinnat kyselyssä, sillä ryhmäjakoa tehdessä opiskelijoiden järjestys satunnaistetaan ja algoritmi suosii listassa ensimmäisenä olevaa henkilöä joilla on samat valinnat.
- Kun ryhmäjaon tulokset on tallennettu _et voi enää avata kyselyä uudestaan_ mutta sitä voi käyttää pohjana uudelle kyselylle
- Ryhmäjaon tulokset voi tallentaa Excel-taulukkoon klikkaamalla "Vie tulokset Excel-taulukkoon"-nappia

## 5. Kyselyyn vastaaminen

Vastaussivu näyttää tältä:

<img src="images/answer.png" alt="Answer survey" class="md-image" />

#### 5.1 Vaihtoehtojen järjestäminen

- Raahaa vaihtoehdot vihreään laatikkoon ja järjestä vaihtoehdot mieluisuusjärjestykseen.
- Järjestettävien vaihtoehtojen vähimmäismäärä on ilmoitettu laatikkojen yläpuolella.
- Jos kyselyn luoja on määritellyt vaihtoehdoille lisätietoja, ne saa näkyviin klikkaamalla vaihtoehtoa.

#### 5.2 Vaihtoehtojen kieltäminen

- Jos kyselyn luoja on sallinut vaihtoehtojen kiltämisen, voit kieltää vaihtoehtoja rehaamalla ne punaiseen laatikkoon.
- Vaihtoehtojen kieltämiseen vaaditaan vähintään 10 merkki pitä perustelu, joka tulee kirjoittaa punaisen laatikon alapuolella olevaan laatikkoon.

## 6. Monivaiheiseen kyselyyn vastaaminen

Monivaiheisen kyselyn vastuassivu näyttää tältä:

<img src="images/multistage_answer.png" alt="Multi-stage answer" class="md-image" />

#### 6.1 Vaiheet monivaiheisessa kyselyssä

- Vaiheet on listattu kyselyn nimen ja lisätietojen alla.
- Vaiheiden välillä voi navigoida klikkaamalla vaiheen tunnistetta.
- Vastaa jokaiseen vaiheeseen kuten tavallisessa kyselyssä:
  - Raahaa vaihtoehdot vihreään laatikkoon ja järjestä vaihtoehdot mieluisuusjärjestykseen.
  - Jos kyselyn luoja on sallinut vaihtoehtojen kiltämisen, voit kieltää vaihtoehtoja rehaamalla ne punaiseen laatikkoon.

#### 6.2 Poissaolot

- Poissaolevaksi ilmoittautuminen on mahdollista vain, jos kyselyn luoja on sallinut sen
  - Tällöin vaiheen yläreunaan ilmestyy "En ole paikalla tässä vaiheessa" nappi, jota painamalla voit ilmoittautua poissaolevaksi

<img src="images/absence.png" alt="Absence" class="md-image" />
