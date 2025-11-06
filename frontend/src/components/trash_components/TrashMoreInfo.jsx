import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import manageSearchIcon from "/images/manage_search_white_36dp.svg";
import folderCopyIcon from "/images/folder_copy_white_36dp.svg";
import deleteIcon from "/images/delete_white_36dp.svg";
import restoreIcon from "/images/restore_from_trash_36d.svg";

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
          src={restoreIcon}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Palauta kysely")}
      </span>
      <br></br>
      <Link className="surveys_link" to={`/surveys/${survey.id}/answers`}>
        <img
          src={manageSearchIcon}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Tarkastele tuloksia")}
      </Link>
      <br></br>
      <Link
        className="surveys_link"
        to={`/surveys/create?fromtemplate=${survey.id}`}
      >
        <img
          src={folderCopyIcon}
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
          src={deleteIcon}
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
