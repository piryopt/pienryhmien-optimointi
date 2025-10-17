import SurveyTableRow from "./SurveyTableRow";
import SurveyTableHeaders from "./SurveyTableHeaders";
import surveyService from "../../serivces/surveys";

const SurveysTable = ({ activeSurveys, closedSurveys, setActiveSurveys, setClosedSurveys }) => {
  const handleDeleteClick = async (surveyId, closedStatus) => {
    if (window.confirm("Haluatko varmasti poistaa kyselyn?")) {
      try {
        await surveyService.deleteSurvey(surveyId)
        if (!closedStatus) {
          const updatedSurveys = activeSurveys.filter(s => s.id !== surveyId)
          setActiveSurveys(updatedSurveys)
        } else {
          const updatedSurveys = closedSurveys.filter(s => s.id !== surveyId)
          setClosedSurveys(updatedSurveys)
        }
      } catch (err) {
        console.error("Error deleting survey:", err)
      }
    };
  };
  
  return (
    <table className="table table-striped">
      <thead className="table-dark">
          <SurveyTableHeaders />
      </thead>
      <tbody>
        {activeSurveys.map((survey, i) => 
            <SurveyTableRow 
              survey={survey}
              key={i}
              handleDeleteClick={handleDeleteClick}
            />
        )}
        <tr>
          <td>---</td>
          <td>---</td>
          <td>---</td>
          <td>---</td>
          <td>---</td>
        </tr>
        {closedSurveys.map((survey, i) => 
          <SurveyTableRow 
            survey={survey}
            key={i}
            handleDeleteClick={handleDeleteClick}
          />
        )}
      </tbody>
    </table>
  )
}

export default SurveysTable;