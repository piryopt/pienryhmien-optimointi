import { useTranslation } from "react-i18next";
import { useState, useEffect } from "react";
import surveyService from "../../services/surveys";
import UserRankings from "../UserRankings";
import { imagesBaseUrl } from "../../utils/constants";

const SurveyResultsTableRow = ({ result, surveyId, currStage }) => {
  const [rankingsVisible, setRankingsVisible] = useState(false);
  const [rankings, setRankings] = useState([]);
  const [rejections, setRejections] = useState([]);
  const [ordinal, setOrdinal] = useState(result[3])
  const { t } = useTranslation();

  useEffect(() => {
    let mounted = true
    const computeOrdinal = async () => {
      try {
        const resp = await surveyService.getStudentRankings(
          surveyId,
          result[1], // email
          currStage
        )

        const normalize = (arr) =>
          (arr || []).map((c) =>
            typeof c === "object"
              ? String(c.id ?? c.choice_id ?? c[0] ?? "")
              : String(c)
          )

        const rankingIds = normalize(resp.choices)
        const RejectionIds = normalize(resp.rejections)

        const allocatedChoiceId = String(result[2][0])

        const idx = rankingIds.indexOf(allocatedChoiceId)
        let ord
        if (idx !== -1) {
          ord = idx + 1
        } else if (RejectionIds.indexOf(allocatedChoiceId) !== -1) {
          ord = t("Hylätty")
        } else {
          ord = t("Ei järjestetty")
        }

        if (mounted) {
          setOrdinal(ord)
          setRankings(resp.choices || [])
          setRejections(resp.rejections || [])
        }
      } catch (err) {
        console.error("Error computing ordinal", err)
      }
    }

    computeOrdinal()
    return () => {
      mounted = false
    }
  }, [surveyId, result, currStage, t])

  const handleRankingClick = async () => {
    try {
      if (rankings.length === 0 && rejections.length === 0) {
        const response = await surveyService.getStudentRankings(
          surveyId,
          result[1], // email
          currStage
        );
        setRankings(response.choices);
        setRejections(response.rejections);
      }
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
        <p style={rankingStyle}>{ordinal}</p>
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
