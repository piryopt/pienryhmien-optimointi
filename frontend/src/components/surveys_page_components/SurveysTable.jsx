import SurveyTableRow from "./SurveyTableRow";

const SurveysTable = ({ activeSurveys, closedSurveys }) => {
  return (
    <table className="table table-striped">
      <thead className="table-dark">
        <tr>
          <td>Kysely</td>
          <td>Kyselyn tila</td>
          <td>Ryhmät luotu</td>
          <td style={{"min-width": "22em"}}>Toiminnot</td>
          <td>Vastausaika päättyy</td>
        </tr>
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