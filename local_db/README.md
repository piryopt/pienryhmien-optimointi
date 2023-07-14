Paikallinen tietokanta pyörii Docker-kontissa. Käynnistä ensin tietokanta tässä hakemistossa olevalla bash-skriptillä. Sen jälkeen aja flask-sovellus yhtä hakemistoa ylempänä olevalla run_flask_app-skriptillä.
Molemmat skriptit luovat tarvittavat ympäristömuuttujat ja tunnukset testitietokannalle. HUOM! Nämä tunnukset ovat vain pientä paikallista testaamista varten, älä käsittele arkaluontoista dataa paikalliseslla
tietokannalla.


Riippuen omasta kehitysympärisöstä, joudut ehkä ajamaan tämän skriptin sudo-ryhmän oikeuksin. Siksi ehkä joudut ajamaan skriptin: sudo ./build-and-run-db.sh
Docker nimittäin oletuksena vaatii root-oikeuksia konttien rakentamiseen ja ajamiseen. 
