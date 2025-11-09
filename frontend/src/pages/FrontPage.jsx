import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import surveyService from "../services/surveys.js";
import listIcon from "/images/list_white_36dp.svg";
import addIcon from "/images/note_add_white_36dp.svg";
import multiAddIcon from "/images/note_stack_add_36dp.svg";
import surveyIcon from "/images/assignment_white_36dp.svg";
import trashIcon from "/images/delete_36dp.svg";

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
      <div className="d-flex w-100">
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
          <small className="text-muted text-nowrap">
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
  const [trashCount, setTrashCount] = useState(0);
  const [activeSurveys, setActiveSurveys] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    const getFrontPageData = async () => {
      try {
        const responseData = await surveyService.getFrontPageData();
        setCreatedSurveys(responseData.createdSurveys);
        setActiveSurveys(responseData.activeSurveys);
        setTrashCount(responseData.trashCount);
      } catch (err) {
        console.error("Error fetching data", err);
      }
    };
    getFrontPageData();
  }, []);

  return (
    <>
      <p>{t("Toiminnot")}</p>
      <div className="row mb-5">
        <div className="col-sm">
          <FrontPageButton
            path="/surveys/create"
            imgSrc={addIcon}
            mainText="Luo uusi kysely"
            additionalText="Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta"
          />
          <br></br>
          <FrontPageButton
            path="multistage/survey/create"
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
          <br></br>
          <FrontPageButton
            path="/trash"
            imgSrc={trashIcon}
            mainText="Roskakori"
            additionalText="Näe poistettavaksi asetetut kyselyt"
            topRightText="Poistettavat kyselyt"
            additionalVars={{ count: trashCount }}
          />
        </div>
      </div>
      <p>{t("Käynnissä olevat kyselyt")}</p>
      <div className="row">
        <div className="col-sm">
          {activeSurveys.map((survey) => (
            <div key={survey.id} className="mb-4">
              <FrontPageButton
                key={survey.id}
                path={
                  survey.is_multistage
                    ? `surveys/multistage/${survey.id}`
                    : `surveys/${survey.id}`
                }
                imgSrc={surveyIcon}
                mainText={survey.surveyname}
                additionalText="Vastaukset"
                topRightText="etusivu.Vastausaika päättyy"
                additionalVars={{
                  timeEnd: survey.time_end,
                  count: survey.response_count
                }}
              />
            </div>
          ))}
          <br></br>
        </div>
      </div>
    </>
  );
};

export default FrontPage;
