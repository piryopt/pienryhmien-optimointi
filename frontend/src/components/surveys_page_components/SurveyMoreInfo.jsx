import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import manageSearchWhite from "/images/manage_search_white_36dp.svg";
import contentCopyWhite from "/images/content_copy_white_36dp.svg";
import editWhite from "/images/edit_white_36dp.svg";
import folderCopyWhite from "/images/folder_copy_white_36dp.svg";
import deleteWhite from "/images/delete_white_36dp.svg";

const SurveyMoreInfo = ({ survey, handleDeleteClick }) => {
  const { t } = useTranslation();
  const handleCopyUrlClick = () => {
    const currUrl = window.location.href;
    navigator.clipboard.writeText(`${currUrl}/${survey.id}`);
  };

  return (
    <div>
      <Link className="surveys_link" to={`/surveys/${survey.id}/answers`}>
        <img
          src={manageSearchWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Tarkastele tuloksia")}
      </Link>
      {!survey.closed && (
        <>
          <br />
          <span
            className="surveys_link"
            onClick={handleCopyUrlClick}
            style={{ cursor: "pointer" }}
          >
            <img
              src={contentCopyWhite}
              alt=""
              className="d-inline-block align-text-top"
              width="20"
              height="20"
            />
            &nbsp;{t("Kopioi kyselyn osoite leikepöydälle")}
          </span>
        </>
      )}
      <br></br>
      <Link to={`/surveys/${survey.id}/edit`} className="surveys_link">
        <img
          src={editWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Muokkaa kyselyä tai lisää siihen ylläpitäjä")}
      </Link>
      <br></br>
      <Link
        className="surveys_link"
        to={`/surveys/create?fromtemplate=${survey.id}`}
      >
        <img
          src={folderCopyWhite}
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
          src={deleteWhite}
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

export default SurveyMoreInfo;
