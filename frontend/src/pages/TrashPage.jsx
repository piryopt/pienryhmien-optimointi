import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import TrashTable from "../components/trash_components/TrashTable.jsx";
import { imagesBaseUrl } from "../utils/constants";

const TrashPage = () => {
  const [surveys, setSurveys] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    const getSurveys = async () => {
      try {
        const responseData = await surveyService.getDeletedSurveys();
        setSurveys(responseData);
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
          src={`${imagesBaseUrl}/delete_36dp.svg`}
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
