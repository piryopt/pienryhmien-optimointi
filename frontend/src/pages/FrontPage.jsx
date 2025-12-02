import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import FrontPageButton from "../components/FrontPageButton.jsx";
import surveyService from "../services/surveys.js";
import { useAuth } from "../context/AuthProvider";
import { imagesBaseUrl } from "../utils/constants.js";

const FrontPage = () => {
  const [createdSurveys, setCreatedSurveys] = useState(0);
  const [trashCount, setTrashCount] = useState(0);
  const [activeSurveys, setActiveSurveys] = useState([]);
  const { t } = useTranslation("front");
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
      <p>{t("actions")}</p>
      <div className="row mb-5">
        <div className="col-sm">
          <FrontPageButton
            path="/surveys/create"
            imgSrc={`${imagesBaseUrl}/note_add_white_36dp.svg`}
            mainText={t("createSurvey")}
            additionalText={t("createSurveyDescription")}
          />
          <br></br>
          <FrontPageButton
            path="/surveys/multistage/create"
            imgSrc={`${imagesBaseUrl}/note_stack_add_36dp.svg`}
            mainText={t("createMultiStageSurvey")}
            additionalText={t("createMultiStageSurveyDescription")}
          />
        </div>
        <div className="col-sm">
          <FrontPageButton
            path="/surveys"
            imgSrc={`${imagesBaseUrl}/list_white_36dp.svg`}
            mainText={t("showAllSurveys")}
            additionalText="createdSurveys"
            additionalVars={{ count: createdSurveys }}
          />
          <br></br>
          <FrontPageButton
            path="/trash"
            imgSrc={`${imagesBaseUrl}/delete_36dp.svg`}
            mainText={t("trashBin")}
            additionalText={t("showTrashedSurveys")}
            topRightText="surveysToBeDeleted"
            additionalVars={{ count: trashCount }}
          />
          {/* Admin-only link */}
          {isAdmin && (
            <>
              <br />
              <FrontPageButton
                path="/admintools/analytics"
                imgSrc={`${imagesBaseUrl}/list_white_36dp.svg`}
                mainText={t("adminTools")}
                additionalText={t("openAdminTools")}
              />
            </>
          )}
        </div>
      </div>
      <p>{t("activeSurveys")}</p>
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
                additionalText="answers"
                topRightText="responseTimeEnd"
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
