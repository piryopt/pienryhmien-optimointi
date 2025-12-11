import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import { useNotification } from "../../context/NotificationContext";
import { imagesBaseUrl } from "../../utils/constants";

const SurveyMoreInfo = ({ survey, handleDeleteClick }) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();

  const handleCopyUrlClick = () => {
    const currUrl = window.location.href;
    navigator.clipboard.writeText(
      survey.is_multistage
        ? `${currUrl}/multistage/${survey.id}`
        : `${currUrl}/${survey.id}`
    );
    showNotification(t("Kyselyn osoite kopioitu leikepöydälle"), "success");
  };

  return (
    <div>
      <Link
        className="surveys_link"
        to={
          survey.is_multistage
            ? `/surveys/multistage/${survey.id}/answers`
            : `/surveys/${survey.id}/answers`
        }
      >
        <img
          src={`${imagesBaseUrl}/manage_search_white_36dp.svg`}
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
              src={`${imagesBaseUrl}/content_copy_white_36dp.svg`}
              alt=""
              className="d-inline-block align-text-top"
              width="20"
              height="20"
            />
            &nbsp;{t("Kopioi kyselyn osoite leikepöydälle")}
          </span>
        </>
      )}
      <br />
      <Link to={`/surveys/${survey.id}/edit`} className="surveys_link">
        <img
          src={`${imagesBaseUrl}/edit_white_36dp.svg`}
          alt=""
          className="d-inline-block align-text-top"
          width="20"
          height="20"
        />
        &nbsp;{t("Muokkaa kyselyä tai lisää siihen ylläpitäjä")}
      </Link>
      <br />
      <Link
        className="surveys_link"
        to={
          survey.is_multistage
            ? `/surveys/multistage/create?fromtemplate=${survey.id}`
            : `/surveys/create?fromtemplate=${survey.id}`
        }
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
      <br />
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

export default SurveyMoreInfo;
