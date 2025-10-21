import { useTranslation } from "react-i18next";
import SurveyAnswersTableHeaders from "./SurveyAnswersTableHeaders";
import SurveyAnswersTableRow from "./SurveyAnswersTableRow";
import surveyService from "../../services/surveys";

const SurveyAnswersTable = (props) => {
  const { t } = useTranslation();
  const handleAnswerDelete = (email) => {
    if (window.confirm(t("Haluatko varmasti poistaa vastauksen?"))) {
      try {
        surveyService.deleteSurveyAnswer(props.surveyId, email)
        const updatedAnswers = props.answers.filter(a => a.email !== email);
        props.setAnswers(updatedAnswers);
        props.setSurveyAnswersAmount(prev => prev - 1);
      } catch (err) {
        console.error("Error deleting answer:", err);
      }
    }
  }
  
  return (
    <table cellSpacing={10} className="table table-striped">
      <thead className="table-dark">
        <SurveyAnswersTableHeaders />
      </thead>
      <tbody>
        {props.answers.map((answer, i) => 
          <SurveyAnswersTableRow 
            answer={answer} 
            handleAnswerDelete={handleAnswerDelete}
            surveyId={props.surveyId}
            key={i}
          />
        )}
      </tbody>
    </table>
  )
};

export default SurveyAnswersTable;