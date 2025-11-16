import { useTranslation } from "react-i18next";
import { useState } from "react";
import { Link } from "react-router-dom";
import TrashMoreInfo from "./TrashMoreInfo";
import { imagesBaseUrl } from "../../utils/constants";

const TrashTableRow = ({ survey, handleDeleteClick, handleRestoreClick }) => {
  const [moreInfoVisible, setMoreInfoVisible] = useState(!survey.closed);
  const { t } = useTranslation();

  const timestamp = Date.parse(survey.deleted_at);
  const timeDate = new Date(timestamp);
  const nextWeek = new Date();
  nextWeek.setDate(timeDate.getDate() + 7);

  const day = nextWeek.getDate();
  const month = nextWeek.getMonth() + 1;
  const year = nextWeek.getFullYear();

  const deleteDate = `${day}.${month}.${year}`;

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
            survey.closed
              ? `${imagesBaseUrl}/insert_page_break_white_36dp.svg`
              : `${imagesBaseUrl}/insert_drive_file_white_36dp.svg`
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
              src={`${imagesBaseUrl}/menu_white_36dp.svg`}
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
          <TrashMoreInfo
            survey={survey}
            handleDeleteClick={handleDeleteClick}
            handleRestoreClick={handleRestoreClick}
          />
        )}
      </td>
      <td>{deleteDate}</td>
    </tr>
  );
};

export default TrashTableRow;
