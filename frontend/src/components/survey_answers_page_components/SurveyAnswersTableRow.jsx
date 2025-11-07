import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import surveyService from "../../services/surveys";
import menuWhite from "/images/menu_white_36dp.svg";
import deleteWhite from "/images/delete_white_36dp.svg";
import UserRankings from "../UserRankings";

const SurveyAnswersTableRow = ({
  answer,
  handleAnswerDelete,
  surveyId,
  stage = null
}) => {
  const [rankingsVisible, setRankingsVisible] = useState(false);
  const [rankings, setRankings] = useState([]);
  const [rejections, setRejections] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    setRankingsVisible(false);
  }, [stage]);

  const handleRankingClick = async () => {
    try {
      const response = await surveyService.getStudentRankings(
        surveyId,
        answer.email,
        stage
      );
      console.log(response);
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
        <span
          className="surveys_link"
          style={{ cursor: "pointer" }}
          onClick={handleRankingClick}
        >
          <img src={menuWhite} alt="" width={20} height={20} />
          &nbsp;{rankingsVisible ? t("Piilota") : t("Näytä")}
        </span>
        {rankingsVisible && (
          <UserRankings rankings={rankings} rejections={rejections} />
        )}
      </td>
      <td>
        <p>{answer.reason}</p>
      </td>
      <td>
        <span
          style={{ cursor: "pointer" }}
          className="surveys_link"
          onClick={() => handleAnswerDelete(answer.email)}
        >
          <img src={deleteWhite} alt="" width={30} height={24} />
        </span>
      </td>
    </tr>
  );
};

export default SurveyAnswersTableRow;
