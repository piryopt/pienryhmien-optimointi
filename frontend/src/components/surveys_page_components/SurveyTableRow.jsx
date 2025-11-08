import { useTranslation } from "react-i18next";
import { useState } from "react";
import SurveyMoreInfo from "./SurveyMoreInfo";
import menu_white from "/images/menu_white_36dp.svg";
import insertDriveFileWhite from "/images/insert_drive_file_white_36dp.svg";
import insertPageBreakWhite from "/images/insert_page_break_white_36dp.svg";
import noteStack from "/images/note_stack_36dp.svg";
import { Link } from "react-router-dom";

const SurveyTableRow = ({ survey, handleDeleteClick }) => {
  const [moreInfoVisible, setMoreInfoVisible] = useState(!survey.closed);
  const { t } = useTranslation();

  if (survey.id === "separatingRow") {
    return (
      <tr>
        <td>---</td>
        <td>---</td>
        <td>---</td>
        <td>---</td>
        <td>---</td>
      </tr>
    );
  }
  return (
    <tr>
      <td>
        <img
          src={
            survey.is_multistage
              ? noteStack
              : survey.closed
                ? insertPageBreakWhite
                : insertDriveFileWhite
          }
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        <Link
          className="surveys_link"
          to={
            survey.is_multistage
              ? `/surveys/multistage/${survey.id}`
              : `/surveys/${survey.id}`
          }
        >
          &nbsp;
          {survey.surveyname}
        </Link>
      </td>
      <td>
        <p style={{ color: survey.closed ? "orangered" : "green" }}>
          {survey.closed ? t("Suljettu") : t("Avoin")}
        </p>
      </td>
      <td>
        <p style={{ color: survey.results_saved && "green" }}>
          {survey.results_saved ? t("Kyllä") : t("Ei")}
        </p>
      </td>
      <td>
        <div onClick={() => setMoreInfoVisible(!moreInfoVisible)}>
          <label style={{ cursor: "pointer" }} className="surveys_link">
            <img
              src={menu_white}
              alt=""
              className="d-inline-block align-text-top"
              width="20"
              height="20"
            />
            &nbsp;
            {moreInfoVisible ? t("Piilota") : t("Näytä")}
          </label>
        </div>
        {moreInfoVisible && (
          <SurveyMoreInfo
            survey={survey}
            handleDeleteClick={handleDeleteClick}
          />
        )}
      </td>
      <td>{survey.time_end}</td>
    </tr>
  );
};

export default SurveyTableRow;
