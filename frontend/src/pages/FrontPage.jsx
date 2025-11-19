import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import surveyService from "../services/surveys.js";
import { useAuth } from "../context/AuthProvider";
import { imagesBaseUrl } from "../utils/constants.js";

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
  const { user, loading } = useAuth();
  const isAdmin = !loading && user && user.admin;

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
            imgSrc={`${imagesBaseUrl}/note_add_white_36dp.svg`}
            mainText="Luo uusi kysely"
            additionalText="Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta"
          />
          <br></br>
          <FrontPageButton
            path="/surveys/multistage/create"
            imgSrc={`${imagesBaseUrl}/note_stack_add_36dp.svg`}
            mainText="Luo uusi monivaiheinen kysely"
            additionalText="Luo uusi monivaiheinen kysely, jossa määritetään eri vaiheiden vastausvaihtoehdot"
          />
        </div>
        <div className="col-sm">
          <FrontPageButton
            path="/surveys"
            imgSrc={`${imagesBaseUrl}/list_white_36dp.svg`}
            mainText="Näytä vanhat kyselyt"
            additionalText="Luotuja kyselyitä"
            additionalVars={{ count: createdSurveys }}
          />
          <br></br>
          <FrontPageButton
            path="/trash"
            imgSrc={`${imagesBaseUrl}/delete_36dp.svg`}
            mainText="Roskakori"
            additionalText="Näe poistettavaksi asetetut kyselyt"
            topRightText="Poistettavat kyselyt"
            additionalVars={{ count: trashCount }}
          />
          {/* Admin-only link */}
          {isAdmin && (
            <>
              <br />
              <FrontPageButton
                path="/admintools/analytics"
                imgSrc={`${imagesBaseUrl}/list_white_36dp.svg`}
                mainText="Hallintatyökalut"
                additionalText="Avaa järjestelmänhallintanäkymä"
              />
            </>
          )}
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
                imgSrc={`${imagesBaseUrl}/assignment_white_36dp.svg`}
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
