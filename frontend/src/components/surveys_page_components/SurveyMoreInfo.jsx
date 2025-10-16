import surveyService from "../../serivces/surveys";
import manageSearchWhite from "../../static/images/manage_search_white_36dp.svg";
import contentCopyWhite from "../../static/images/content_copy_white_36dp.svg";
import editWhite from "../../static/images/edit_white_36dp.svg";
import folderCopyWhite from "../../static/images/folder_copy_white_36dp.svg";
import deleteWhite from "../../static/images/delete_white_36dp.svg";

const SurveyMoreInfo = ({ survey }) => {
  const handleCopyUrlClick = () => {
    const currUrl = window.location.href;
    navigator.clipboard.writeText(`${currUrl}/${survey.id}`);
  }
  
  const handleDeleteClick = () => {
    if (window.confirm("Haluatko varmasti poistaa kyselyn?")) {
      surveyService
        .deleteSurvey(survey.id)
        .catch(err => {
          console.error("Error deleting survey", err);
        });
    };
  };

  return (
    <div>
      <a 
        className="surveys_link"
        href={`${survey.id}/answers`}
        >
        <img 
          src={manageSearchWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;Tarkastele tuloksia
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
            &nbsp;Kopioi kyselyn osoite leikepöydälle
          </a>
        </>
      }
      <br></br>
      <a
        href={`${survey.id}/edit`}
        className="surveys_link"
        >
        <img 
          src={editWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;Muokkaa kyselyä tai lisää siihen ylläpitäjä
      </a>
      <br></br>
      <a
        className="surveys_link"
        href={`create?fromtemplate=${survey.id}`}
        >
        <img 
          src={folderCopyWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;Kopioi kysely
      </a>
      <br></br>
      <a
        style={{"cursor": "pointer"}}
        className="surveys_link"
        onClick={handleDeleteClick}
        >
        <img 
          src={deleteWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;Poista kysely
      </a>
    </div>
  );
};

export default SurveyMoreInfo;