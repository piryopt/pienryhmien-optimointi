import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import SurveysTable from "../components/surveys_page_components/SurveysTable";
import { imagesBaseUrl } from "../utils/constants";

const SurveysPage = () => {
  const [surveys, setSurveys] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    const getSurveys = async () => {
      try {
        const [activeRes, closedRes] = await Promise.all([
          surveyService.getActiveSurveys(),
          surveyService.getClosedSurveys()
        ]);
        const separatingRow = { id: "separatingRow" };
        const updatedSurveys = [...activeRes, separatingRow, ...closedRes];
        setSurveys(updatedSurveys);
      } catch (err) {
        console.error("Error loading surveys", err);
      }
    };
    getSurveys();
  }, []);

  return (
    <div>
      <br />
      <h2>
        <img
          src={`${imagesBaseUrl}/list_white_36dp.svg`}
          alt=""
          className="d-inline-block align-text-top"
          width="42"
          height="47"
        />
        &nbsp;{t("Aiemmat kyselyt")}
      </h2>
      <br />
      <SurveysTable surveys={surveys} setSurveys={setSurveys} />
    </div>
  );
};

export default SurveysPage;
