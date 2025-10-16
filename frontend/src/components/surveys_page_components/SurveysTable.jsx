import SurveyTableRow from "./SurveyTableRow";
import SurveyTableHeaders from "./SurveyTableHeaders";

const SurveysTable = ({ activeSurveys, closedSurveys }) => {
  return (
    <table className="table table-striped">
      <thead className="table-dark">
          <SurveyTableHeaders />
      </thead>
      <tbody>
        {activeSurveys.map((survey, i) => 
            <SurveyTableRow survey={survey} key={i} />
        )}
        <tr>
          <td>---</td>
          <td>---</td>
          <td>---</td>
          <td>---</td>
          <td>---</td>
        </tr>
        {closedSurveys.map((survey, i) => 
          <SurveyTableRow survey={survey} key={i} />
        )}
      </tbody>
    </table>
  )
}

export default SurveysTable;