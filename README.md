# Jakaja-sovellus pienryhmien optimointiin
![GHA workflow badge](https://github.com/piryopt/pienryhmien-optimointi/workflows/CI/badge.svg)

Tämä on Helsingin yliopiston [Ohjelmistotuotantoprojekti-kurssin](https://studies.helsinki.fi/opintotarjonta/cur/otm-96ddc0a9-a15b-4717-bfdc-23872092b730/TKT20007/_Ohjelmistotuotantoprojekti_) lopputuotteen repositorio. 

Sovelluksen tilaaja on Helsingin yliopiston kasvatustieteellinen tiedekunta. Haasteena on suurten opiskelijamäärien jakaminen ryhmiin. Aikaisemmin ryhmäjako on tehty käsin Excel-taulukkoja pyörittelemällä, mikä on hidasta ja työlästä. Avoimesti tarjolla olevat sovellusratkaisut eivät sovellu  suurille ryhmille ja poikkeuksien huomiointi on niissä vaikeaa. Asian korjaamiseksi on tilattu sovellus, jolla opiskelija voi ilmoittaa toiveensa ja opettaja voi jakaa ryhmät.

Jakaja-sovellus hyödyntää [unkarilaista algoritmiä](https://en.wikipedia.org/wiki/Hungarian_algorithm), jonka avulla opiskelijat voidaan jakaa ryhmiin tehokkaasti ja optimaalisesti. Opettaja voi luoda sovelluksessa kyselyn, johon hän pyytää opiskelijoita vastaamaan. Opiskelija ilmoittaa kyselyllä mielipiteensä, esimerkiksi asettaa haluamansa ryhmätyöaiheet toivomusjärjestykseen. Kyselyn päätyttyä opettaja pyytää sovellusta suorittamaan lajittelun ja saa tulokset taulukkomuodossa. Tavoitteena on nopea, tehokas ja ryhmän kannalta mahdollisimman optimaalinen ryhmäjako.
