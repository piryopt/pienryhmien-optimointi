import { useTranslation } from "react-i18next";
import { useState } from "react";
import surveyService from "../../services/surveys";
import UserRankings from "../UserRankings";
import { imagesBaseUrl } from "../../utils/constants";

const SurveyResultsTableRow = ({ result, surveyId }) => {
  const [rankingsVisible, setRankingsVisible] = useState(false);
  const [rankings, setRankings] = useState([]);
  const [rejections, setRejections] = useState([]);
  const { t } = useTranslation();

  const handleRankingClick = async () => {
    try {
      const response = await surveyService.getStudentRankings(
        surveyId,
        result[1] // email
      );
      setRankings(response.choices);
      setRejections(response.rejections);
      setRankingsVisible(!rankingsVisible);
    } catch (err) {
      console.error("Error showing rankings", err);
    }
  };

  const rankingStyle = {
    color:
      result[3] === "Hylätty"
        ? "red"
        : result[3] === "Ei järjestetty"
          ? "yellow"
          : ""
  };

  return (
    <tr>
      {/* result = [[userId, username], email, [surveyChoiceId, surveyChoiceName], ordinalChoice] */}
      <td>
        <p>{result[0][1]}</p>
      </td>
      <td>
        <p>{result[1]}</p>
      </td>
      <td>
        <p>{result[2][1]}</p>
      </td>
      <td>
        <p style={rankingStyle}>{result[3]}</p>
      </td>
      <td>
        <span
          className="surveys_link"
          style={{ cursor: "pointer" }}
          onClick={handleRankingClick}
        >
          <img
            src={`${imagesBaseUrl}/menu_white_36dp.svg`}
            alt=""
            width={20}
            height={20}
          />
          &nbsp;{rankingsVisible ? t("Piilota") : t("Näytä")}
        </span>
        {rankingsVisible && (
          <UserRankings rankings={rankings} rejections={rejections} />
        )}
      </td>
    </tr>
  );
};

export default SurveyResultsTableRow;
