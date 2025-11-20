import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import SurveyAnswersTable from "../components/survey_answers_page_components/SurveyAnswersTable";
import StageDropdown from "../components/survey_answers_page_components/StageDropdown";
import SurveyAnswersInfo from "../components/survey_answers_page_components/SurveyAnswersInfo";
import AnswersButtons from "../components/survey_answers_page_components/AnswersButtons";
import { imagesBaseUrl } from "../utils/constants";

const SurveyMultistageAnswersPage = () => {
  const { surveyId } = useParams();
  const { t } = useTranslation();

  const [surveyData, setSurveyData] = useState({});
  const [surveyClosed, setSurveyClosed] = useState(false);
  const [surveyAnswers, setSurveyAnswers] = useState([]);
  const [filteredAnswers, setFilteredAnswers] = useState([]);
  const [stages, setStages] = useState([]);
  const [currStage, setCurrStage] = useState(null);
  const [currStageAvailableSpaces, setCurrStageAvailableSpaces] = useState(0);
  const [spacesData, setSpacesData] = useState({});
  const [searchEmail, setSearchEmail] = useState("");
  const [answersAmount, setAnswersAmount] = useState(0);
  const [currAnswers, setCurrAnswers] = useState([]);

  useEffect(() => {
    const getSurveyAnswers = async () => {
      const response =
        await surveyService.getMultiStageSurveyAnswersData(surveyId);
      setSurveyData(response);
      setSurveyAnswers(response.answers);
      setSurveyClosed(response.closed);
      const surveyStages = response.answers.map((s) => Object.keys(s)[0]);
      setStages(surveyStages);
      setFilteredAnswers(response.answers[0][surveyStages[0]]);
      setCurrAnswers(response.answers[0][surveyStages[0]]);
      setCurrStage(surveyStages[0]);
      setCurrStageAvailableSpaces(response.availableSpaces[surveyStages[0]]);
      setAnswersAmount(response.answers[0][surveyStages[0]].length);

      setSpacesData(response.availableSpaces);
    };
    getSurveyAnswers();
  }, []);

  const indexOfCurrStage = () => {
    return surveyAnswers.findIndex((a) => Object.keys(a)[0] === currStage);
  };

  useEffect(() => {
    if (surveyAnswers.length > 0) {
      setFilteredAnswers(surveyAnswers[indexOfCurrStage()][currStage]);
      setSearchEmail("");
    }
  }, [currStage]);

  const handleFilterChange = (event) => {
    const updatedSearchEmail = event.target.value;
    setSearchEmail(updatedSearchEmail);
    const updatedAnswers = surveyAnswers[indexOfCurrStage()][currStage].filter(
      (a) => a.email.includes(updatedSearchEmail.toLowerCase())
    );
    setFilteredAnswers(updatedAnswers);
  };

  return (
    <div>
      <h5>
        <img
          src={`${imagesBaseUrl}/assignment_white_36dp.svg`}
          alt=""
          width={34}
          height={30}
        />
        &nbsp;{surveyData.surveyName}
      </h5>
      <StageDropdown
        stages={stages}
        currStage={currStage}
        setCurrStage={setCurrStage}
        setCurrStageAvailableSpaces={setCurrStageAvailableSpaces}
        spacesData={spacesData}
      />
      <SurveyAnswersInfo
        answersAmount={answersAmount}
        availableSpaces={currStageAvailableSpaces}
      />
      <AnswersButtons
        surveyClosed={surveyClosed}
        setSurveyClosed={setSurveyClosed}
        surveyData={surveyData}
        answers={surveyAnswers}
        surveyId={surveyId}
        multistage={true}
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
      {currStage && (
        <SurveyAnswersTable
          answers={currAnswers}
          setAnswers={setCurrAnswers}
          filteredAnswers={filteredAnswers}
          setFilteredAnswers={setFilteredAnswers}
          surveyId={surveyId}
          setSurveyAnswersAmount={setAnswersAmount}
          stage={currStage}
          stages={stages}
          allAnswers={surveyAnswers}
          setAllAnswers={setSurveyAnswers}
        />
      )}
    </div>
  );
};

export default SurveyMultistageAnswersPage;
