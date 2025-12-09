import { useTranslation } from "react-i18next";
import { imagesBaseUrl } from "../../utils/constants.js";

const JakajaChangelog = () => {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t("Jakajaan tehdyt muutokset versiossa")} 2.0:</h1>
      <br />
      <h4>
        -{" "}
        {t(
          "Jakajan uusimmassa versiossa käyttäjä voi kyselyn luomisvaiheessa määrittää ryhmiä pakollisiksi"
        )}
        ,{" "}
        {t(
          "joihin opiskelijat pyritään sijoittamaan ensisijaisesti valinnoista riippumatta"
        )}
        .
      </h4>
      <img
        src={`${imagesBaseUrl}/jakaja2.0-pakollisetryhmät.png`}
        alt="jakaja pakollisten ryhmien taulukko"
        style={{
          width: "100%",
          maxWidth: "1200px",
          height: "auto",
          display: "block",
          margin: "1rem 0"
        }}
      />
      <br />
      <br />
      <br />
      <h4>
        -{" "}
        {t(
          "Jakajassa on nyt mahdollista myös luoda monivaiheinen kysely, jossa käyttäjä määrittää yksittäisten vaiheiden ryhmävalinnat"
        )}
        ,{" "}
        {t(
          "jolloin ryhmäjako suoritetaan vaihekohtaisesti huomioiden myös mahdolliset pakolliset ryhmät kussakin vaiheessa"
        )}
        .
      </h4>
      <img
        src={`${imagesBaseUrl}/jakaja2.0-monivaiheinen.png`}
        style={{
          width: "100%",
          maxWidth: "1200px",
          height: "auto",
          display: "block",
          margin: "1rem 0"
        }}
      />
      <br />
      <br />
      <br />
      <h4>
        -{" "}
        {t(
          "Monivaiheisen kyselyn luomisvaiheessa käyttäjä voi myös valita sallitaanko vastaajien poissaolo"
        )}
        ,{" "}
        {t(
          "jolloin vastaajat voivat merkitä itsensä poissaolevaksi vastaamislomakkeessa valitsemastaan vaiheesta"
        )}
        .{" "}
        {t("Tällöin vastaajaa ei oteta huomioon kyseisen vaiheen ryhmäjaossa")}.
      </h4>
      <img
        src={`${imagesBaseUrl}/jakaja2.0-poissaolot.png`}
        style={{
          width: "100%",
          maxWidth: "900px",
          height: "auto",
          display: "block",
          margin: "1rem 0"
        }}
      />
      <br />
      <br />
      <h4>
        -{" "}
        {t(
          "Monivaiheisen kyselyn luomisvaiheessa käyttäjä voi myös rajoittaa tietyn ryhmän vastaajien osallistumiskertojen määrää, mikä huomioidaan vastaavasti ryhmäjaossa kyseisen rajoitetun ryhmän kohdalla"
        )}
        .
      </h4>
      <img
        src={`${imagesBaseUrl}/jakaja2.0-osallistumiskerrat.png`}
        style={{
          width: "100%",
          maxWidth: "1200px",
          height: "auto",
          display: "block",
          margin: "1rem 0"
        }}
      />
      <br />
      <br />
      <br />
      <h4>
        -{" "}
        {t(
          "Jakajaan on lisätty myös roskakori, johon kyselyt päätyvät poistaessasi niitä"
        )}
        .{" "}
        {t(
          "Roskakorissa olevan kyselyn voi tarvittaessa palauttaa tai kopioida"
        )}
        .{" "}
        {t("Yli viikon roskakorissa olevat kyselyt poistetaan automaattisesti")}
      </h4>
      <img
        src={`${imagesBaseUrl}/jakaja2.0-trashbin.png`}
        style={{
          width: "100%",
          maxWidth: "1200px",
          height: "auto",
          display: "block",
          margin: "1rem 0"
        }}
      />
    </div>
  );
};

export default JakajaChangelog;
