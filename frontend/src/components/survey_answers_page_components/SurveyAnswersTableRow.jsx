import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import surveyService from "../../services/surveys";
import menuWhite from "/images/menu_white_36dp.svg";
import deleteWhite from "/images/delete_white_36dp.svg";

const SurveyAnswersTableRow = ({ answer, handleAnswerDelete, surveyId }) => {
  const [rankingsVisible, setRankingsVisible] = useState(false);
  const [rankings, setRankings] = useState([]);
  const [rejections, setRejections] = useState([]);
  const { t } = useTranslation();

  const handleRankingClick = async () => {
    try {
      const response = await surveyService.getStudentRankings(
        surveyId,
        answer.email
      );
      setRankings(response.choices);
      setRejections(response.rejections);
      setRankingsVisible(!rankingsVisible);
    } catch (err) {
      console.error("Error showing rankings", err);
    }
  };

  return (
    <tr>
      <td>
        <p>{answer.email}</p>
      </td>
      <td>
        <a
          className="surveys_link"
          style={{ cursor: "pointer" }}
          onClick={handleRankingClick}
        >
          <img src={menuWhite} alt="" width={20} height={20} />
          &nbsp;{rankingsVisible ? t("Piilota") : t("Näytä")}
        </a>
        {rankingsVisible && (
          <div>
            <br />
            <b>{t("Valinnat")}</b>
            <ol>
              {rankings.map((r, i) => (
                <li key={i}>{r.name}</li>
              ))}
            </ol>
            {rejections.length > 0 && (
              <>
                <b>{t("Kielletyt")}</b>
                <ul>
                  {rejections.map((r, i) => (
                    <li key={i}>{r.name}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </td>
      <td>
        <p>{answer.reason}</p>
      </td>
      <td>
        <a
          style={{ cursor: "pointer" }}
          className="surveys_link"
          onClick={() => handleAnswerDelete(answer.email)}
        >
          <img src={deleteWhite} alt="" width={30} height={24} />
        </a>
      </td>
    </tr>
  );
};

export default SurveyAnswersTableRow;
