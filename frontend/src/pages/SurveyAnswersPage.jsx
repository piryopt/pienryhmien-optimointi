import { useEffect, useRef, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import SurveyAnswersTable from "../components/survey_answers_page_components/SurveyAnswersTable";
import SurveyAnswersInfo from "../components/survey_answers_page_components/SurveyAnswersInfo";
import AnswersButtons from "../components/survey_answers_page_components/AnswersButtons";
import { imagesBaseUrl } from "../utils/constants";

const SurveyAnswersPage = () => {
  const [answers, setAnswers] = useState([]);
  const [filteredAnswers, setFilteredAnswers] = useState([]);
  const [surveyData, setSurveyData] = useState({});
  const [surveyAnswersAmount, setSurveyAnswersAmount] = useState(0);
  const [surveyClosed, setSurveyClosed] = useState(false);
  const [searchEmail, setSearchEmail] = useState("");
  const [loading, setLoading] = useState(true);
  const [answersSaved, setAnswersSaved] = useState(false);

  const { id } = useParams();
  const { t } = useTranslation("result");
  const navigate = useNavigate();
  const mountedRef = useRef(false);

  useEffect(() => {
    mountedRef.current = true;
    const getSurveyAnswersData = async () => {
      try {
        const responseData = await surveyService.getSurveyAnswersData(id);
        if (responseData.answersSaved) {
          setAnswersSaved(true);
          navigate(`/surveys/${id}/results`, { replace: true });
          return;
        }
        setAnswers(responseData.surveyAnswers);
        setFilteredAnswers(responseData.surveyAnswers);
        setSurveyData(responseData);
        setSurveyAnswersAmount(Number(responseData.surveyAnswersAmount));
        setSurveyClosed(responseData.closed);
      } catch (err) {
        console.error("Error loading survey data", err);
      } finally {
        if (mountedRef.current) setLoading(false);
      }
    };
    getSurveyAnswersData();
    return () => {
      mountedRef.current = false;
    };
  }, [surveyClosed]);

  const handleFilterChange = (event) => {
    const updatedSearchEmail = event.target.value;
    setSearchEmail(updatedSearchEmail);
    const updatedAnswers = answers.filter((a) =>
      a.email.includes(updatedSearchEmail.toLowerCase())
    );
    setFilteredAnswers(updatedAnswers);
  };

  if (answersSaved) return null;

  if (loading)
    return <div className="text-center mt-5">{t("Ladataan...")}</div>;

  return (
    <div>
      <br />
      <h5>
        <img
          src={`${imagesBaseUrl}/assignment_white_36dp.svg`}
          alt=""
          width={34}
          height={30}
        />
        &nbsp;{surveyData.surveyName}
      </h5>
      <SurveyAnswersInfo
        answersAmount={surveyAnswersAmount}
        availableSpaces={surveyData.availableSpaces}
      />
      <AnswersButtons
        surveyClosed={surveyClosed}
        setSurveyClosed={setSurveyClosed}
        surveyData={surveyData}
        answers={answers}
        surveyId={id}
      />
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
