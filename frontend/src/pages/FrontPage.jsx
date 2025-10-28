import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import surveyService from "../services/surveys.js";
import listIcon from "/images/list_white_36dp.svg";
import addIcon from "/images/note_add_white_36dp.svg";
import multiAddIcon from "/images/note_stack_add_36dp.svg";
import surveyIcon from "/images/assignment_white_36dp.svg";

const FrontPageButton = ({
  path,
  imgSrc,
  mainText,
  additionalText,
  topRightText,
  additionalVars
}) => {
  const { t } = useTranslation();

  return (
    <Link
      to={path}
      className="list-group-item list-group-item-action"
      style={{ borderRadius: "12px" }}
    >
      <div className="d-flex w-100 justify-content-between">
        <div className="d-flex w-100">
          <img
            src={imgSrc}
            alt=""
            width="34"
            height="30"
            className=""
            style={{ marginRight: "8px" }}
          />
          <p style={{ fontSize: "130%" }}>{t(mainText, additionalVars)}</p>
        </div>

        {topRightText && (
          <small className="text-muted">
            {t(topRightText, additionalVars)}
          </small>
        )}
      </div>
      <small className="text-muted">{t(additionalText, additionalVars)}</small>
    </Link>
  );
};

const FrontPage = () => {
  const [createdSurveys, setCreatedSurveys] = useState(0);
  const [activeSurveys, setActiveSurveys] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    const getFrontPageData = async () => {
      try {
        const responseData = await surveyService.getFrontPageData();
        setCreatedSurveys(responseData.createdSurveys);
        setActiveSurveys(responseData.activeSurveys);
      } catch (err) {
        console.error("Error fetching data", err);
      }
    };
    getFrontPageData();
  }, []);

  return (
    <>
      <p>{t("Toiminnot")}</p>
      <div className="row">
        <div className="col-sm">
          <FrontPageButton
            path="/surveys/create"
            imgSrc={addIcon}
            mainText="Luo uusi kysely"
            additionalText="Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta"
          />
          <br></br>
          <FrontPageButton
            path="multiphase/survey/create"
            imgSrc={multiAddIcon}
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
            additionalVars={{ count: createdSurveys }}
          />
        </div>
      </div>
      <p>{t("Käynnissä olevat kyselyt")}</p>

      <div className="row">
        {activeSurveys.map((survey) => (
          <FrontPageButton
            key={survey.id}
            path={`surveys/${survey.id}`}
            imgSrc={surveyIcon}
            mainText={survey.surveyname}
            additionalText="Vastaukset"
            topRightText="Vastausaika päättyy"
            additionalVars={{
              timeEnd: survey.time_end,
              count: survey.response_count
            }}
          />
        ))}
      </div>
    </>
  );
};

export default FrontPage;
