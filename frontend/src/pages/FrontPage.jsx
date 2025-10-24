import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import listIcon from "/images/assignment_white_36dp.svg";

const FrontPageButton = ({ path, imgSrc, mainText, additionalText }) => {
  return (
    <Link
      to={path}
      className="list-group-item list-group-item-action flex-column align-items-start"
      style={{ borderRadius: "12px" }}
    >
      <div className="d-flex w-100 justify-content-between">
        <h5 className="mb-1">
          <img
            src={imgSrc}
            alt=""
            width="34"
            height="30"
            className="d-inline-block align-text-top"
            style={{ marginRight: "8px" }}
          />
          {mainText}
        </h5>
      </div>
      <small className="text-muted">{additionalText}</small>
    </Link>
  );
};

const FrontPage = () => {
  const { t } = useTranslation();

  return (
    <div className="row">
      <div className="col-sm">
        <FrontPageButton
          path="/surveys/create"
          imgSrc={listIcon}
          mainText="Luo uusi kysely"
          additionalText="Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta"
        />
        <FrontPageButton
          path="multiphase/survey/create"
          imgSrc={listIcon}
          mainText="Luo uusi monivaiheinen kysely"
          additionalText="Luo uusi monivaiheinen kysely, jossa määritetään eri vaiheiden vastausvaihtoehdot"
        />
      </div>
      <div className="col-sm">
        <FrontPageButton
          path="/surveys"
          imgSrc={listIcon}
          mainText="Näytä vanhat kyselyt"
          additionalText="Luotuja kyselyitä"
        />
      </div>
    </div>
  );
};

export default FrontPage;
