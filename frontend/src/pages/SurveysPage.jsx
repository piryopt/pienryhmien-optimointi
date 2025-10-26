import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import SurveysTable from "../components/surveys_page_components/SurveysTable";
import listWhite from "/images/list_white_36dp.svg";

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
        const updatedSurveys = [...activeRes, ...closedRes];
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
          src={listWhite}
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
