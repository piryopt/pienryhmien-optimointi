import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import assignmentWhite from "/images/assignment_white_36dp.svg";
import SurveyAnswersTable from "../components/survey_answers_page_components/SurveyAnswersTable";

const SurveyAnswersPage = () => {
  const [answers, setAnswers] = useState([]);
  const [filteredAnswers, setFilteredAnswers] = useState([]);
  const [surveyData, setSurveyData] = useState({});
  const [surveyAnswersAmount, setSurveyAnswersAmount] = useState(0);
  const [surveyClosed, setSurveyClosed] = useState(false);
  const [searchEmail, setSearchEmail] = useState("");
  const [loading, setLoading] = useState(true);

  const { id } = useParams();
  const { t } = useTranslation();
  const navigate = useNavigate();

  useEffect(() => {
    const getSurveyAnswersData = async () => {
      try {
        const responseData = await surveyService.getSurveyAnswersData(id);
        if (responseData.answersSaved)
          navigate(`/surveys/${id}/results`, { replace: true });
        setAnswers(responseData.surveyAnswers);
        setFilteredAnswers(responseData.surveyAnswers);
        setSurveyData(responseData);
        setSurveyAnswersAmount(Number(responseData.surveyAnswersAmount));
        setSurveyClosed(responseData.closed);
      } catch (err) {
        console.error("Error loading survey data", err);
      } finally {
        // fixes bug where the default content flashes before navigation
        setTimeout(() => {
          setLoading(false);
        }, 1);
      }
    };
    getSurveyAnswersData();
  }, [surveyClosed]);

  const handleFilterChange = (event) => {
    const updatedSearchEmail = event.target.value;
    setSearchEmail(updatedSearchEmail);
    const updatedAnswers = answers.filter((a) =>
      a.email.includes(updatedSearchEmail.toLowerCase())
    );
    setFilteredAnswers(updatedAnswers);
  };

  const handleOpenSurveyClick = async () => {
    if (window.confirm(t("Haluatko varmasti avata kyselyn uudestaan?"))) {
      try {
        await surveyService.openSurvey(id);
        setSurveyClosed(false);
        // alert message?
      } catch (err) {
        console.error("error opening survey", err);
      }
    }
  };

  const handleCloseSurveyClick = async () => {
    if (window.confirm(t("Haluatko varmasti sulkea kyselyn?"))) {
      try {
        await surveyService.closeSurvey(id);
        setSurveyClosed(true);
        // alert message?
      } catch (err) {
        console.error("error opening survey", err);
      }
    }
  };

  const handleAssignGroups = () => {
    if (answers.length === 0) {
      // alert message that groups can't be assigned
      return;
    }
    navigate(`/surveys/${id}/results`);
  };

  if (loading) return null;

  return (
    <div>
      <br />
      <h5>
        <img src={assignmentWhite} alt="" width={34} height={30} />
        &nbsp;{surveyData.surveyName}
      </h5>
      <br />
      <i>
        {t("Vastauksia")}: {surveyAnswersAmount}
      </i>
      <br />
      <i>
        {t("Jaettavia paikkoja")}: {surveyData.availableSpaces}
      </i>
      <br />
      <br />
      <Link to="/surveys" className="surveys_link" style={{ float: "right" }}>
        {t("Palaa kyselylistaan")}
      </Link>
      <br />
      <br />
      {surveyClosed ? (
        <>
          <button
            className="btn btn-outline-warning"
            style={{ float: "right" }}
            onClick={handleOpenSurveyClick}
          >
            {t("Avaa kysely uudelleen")}
          </button>
          <button
            className="btn btn-outline-primary"
            onClick={handleAssignGroups}
          >
            {t("Jaa ryhmiin")}
          </button>
        </>
      ) : (
        <button
          className="btn btn-outline-warning"
          style={{ float: "right" }}
          onClick={handleCloseSurveyClick}
        >
          {t("Sulje kysely")}
        </button>
      )}
      <br />
      <br />
      <p>
        <i style={{ whiteSpace: "pre-line" }}>
          {t(`Hae yksittäistä vastausta kirjoittamalla tähän kenttään
            vastaajan sähköposti tai osa siitä`)}
        </i>
        <br />
        <input
          type="email"
          name="search_email"
          id="search_email"
          onChange={handleFilterChange}
          value={searchEmail}
        />
      </p>
      <SurveyAnswersTable
        answers={answers}
        setAnswers={setAnswers}
        filteredAnswers={filteredAnswers}
        setFilteredAnswers={setFilteredAnswers}
        surveyId={id}
        setSurveyAnswersAmount={setSurveyAnswersAmount}
      />
    </div>
  );
};

export default SurveyAnswersPage;
