import { useTranslation } from "react-i18next";
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
  }
  
  return (
    <div>
      <a 
        className="surveys_link"
        href={`/surveys/${survey.id}/answers`}
        >
        <img 
          src={manageSearchWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Tarkastele tuloksia")}
      </a>
      {!survey.closed && 
        <>
          <br />
          <a
            className="surveys_link"
            onClick={handleCopyUrlClick}
            style={{"cursor": "pointer"}}
            >
            <img 
              src={contentCopyWhite}
              alt=""
              className="d-inline-block align-text-top"
              width="20"
              height="20"
            />
            &nbsp;{t("Kopioi kyselyn osoite leikepöydälle")}
          </a>
        </>
      }
      <br></br>
      <a
        href={`/surveys/${survey.id}/edit`}
        className="surveys_link"
        >
        <img 
          src={editWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Muokkaa kyselyä tai lisää siihen ylläpitäjä")}
      </a>
      <br></br>
      <a
        className="surveys_link"
        href={`/surveys/create?fromtemplate=${survey.id}`}
        >
        <img 
          src={folderCopyWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Kopioi kysely")}
      </a>
      <br></br>
      <a
        style={{"cursor": "pointer"}}
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
      </a>
    </div>
  );
};

export default SurveyMoreInfo;