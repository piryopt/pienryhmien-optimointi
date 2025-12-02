# UKK

## Miten ryhmittelyalgoritmi toimii?

- Ryhmäjaon tekemiseen käytetään **unkarilaisena algoritmina** tunnettua menetelmää.
- Kyselyn vastaaja saa järjestää vaihtoehdot sen mukaan, mikä häntä itseään kiinnostaa eniten.
- Valinnat muunnetaan pisteiksi niin, että vastaaja antaa eniten pisteitä sille ryhmälle, jonka on sijoittanut ensimmäiseksi. Vähiten pisteitä saa viimeiseksi sijoitettu tai kokonaan ryhmittelyn ulkopuolelle jäänyt vaihtoehto.
- Unkarilainen algoritmi tekee ryhmäjaon niin, että laskettaessa yhteen vastaajien omalle ryhmälleen antamat pisteet, saadaan mahdollisimman suuri luku.
- Jos jokin ryhmä ei saavuta jaossa sille asetettua minimikokoa, se pudotetaan ja sen opiskelijat siirretään muihin ryhmiin.
- [Jakajan GitHub-sivulta](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/hungarian.md) voit lukea tarkemman (englanninkielisen) selostuksen algoritmin toiminnasta.

## Miten pakolliset ryhmät täytetään?

- Jakaja pudottaa oletusarvoisesti ne ryhmät, jotka eivät ryhmäjaossa täyty minimikokoon asti. Kyselyn laatija voi kuitenkin määrittää ryhmän pakolliseksi. Tällöin kyseinen ryhmä täytetään vähintään minimikokoon asti vastauksista riippumatta.
  - Tämä tarkoittaa, että ryhmään voidaan tarvittaessa sijoittaa myös sellaisia vastaajia, jotka eivät ole valinneet sitä. Ryhmään pyritään kuitenkin ensisijaisesti sijoittamaan ne vastaajat, jotka pitävät siitä eniten.
- Pakolliseen ryhmään voidaan tarvittaessa sijoittaa myös sellainen opiskelija, joka on **kieltänyt** sen.
  - Tämä tehdään vain, jos ryhmän minimikokoa ei saada täyteen sellaisista opiskelijoista, jotka eivät ole kieltäneet ryhmää.
  - Tällöin kyselyn laatijan vastuulla on tarkastella vastaajien perusteluita kiellolle ja arvioida, voidaanko kyseinen opiskelija todella sijoittaa ryhmään.

**HUOM!** Pakollinen ryhmä voidaan kuitenkin edelleen pudottaa jaosta, jos vastaajia on niin vähän, etteivät he riitä täyttämään kaikkia pakollisia ryhmiä minimikokoon asti.

## Mitä uutta löytyy Jakajasta 2.0 löydät [tästä](/jakaja2.0/changelog)

## Minulla on kysyttävää sovelluksesta – kehen voin olla yhteydessä?

Jakajassa on palautesivu, jossa voit kysyä mitä vain.
