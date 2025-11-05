import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import TrashTable from "../components/trash_components/TrashTable.jsx";
import trashIcon from "/images/delete_36dp.svg";

const TrashPage = () => {
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
          src={trashIcon}
          alt=""
          className="d-inline-block align-text-top"
          width="42"
          height="47"
        />
        &nbsp;{t("Roskakori")}
      </h2>
      <br />
      <TrashTable surveys={surveys} setSurveys={setSurveys} />
    </div>
  );
};

export default TrashPage;
