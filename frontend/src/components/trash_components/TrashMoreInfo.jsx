import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { imagesBaseUrl } from "../../utils/constants";

const TrashMoreInfo = ({ survey, handleDeleteClick, handleRestoreClick }) => {
  const { t } = useTranslation();

  return (
    <div>
      <span
        style={{ cursor: "pointer" }}
        className="surveys_link"
        onClick={() => handleRestoreClick(survey.id)}
      >
        <img
          src={`${imagesBaseUrl}/restore_from_trash_36d.svg`}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Palauta kysely")}
      </span>
      <br></br>
      <Link
        className="surveys_link"
        to={`/surveys/${survey.is_multistage ? "multistage/" : ""}create?fromtemplate=${survey.id}`}
      >
        <img
          src={`${imagesBaseUrl}/folder_copy_white_36dp.svg`}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Kopioi kysely")}
      </Link>
      <br></br>
      <span
        style={{ cursor: "pointer" }}
        className="surveys_link"
        onClick={() => handleDeleteClick(survey.id, survey.closed)}
      >
        <img
          src={`${imagesBaseUrl}/delete_white_36dp.svg`}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Poista kysely")}
      </span>
    </div>
  );
};

export default TrashMoreInfo;
