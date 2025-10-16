import SurveyTableRow from "./SurveyTableRow";
import menu_white from "../../static/images/menu_white_36dp.svg";


const SurveysTable = ({ activeSurveys, closedSurveys }) => {
  return (
    <table className="table table-striped">
      <thead className="table-dark">
        <tr>
          <td>Kysely</td>
          <td>Kyselyn tila</td>
          <td>Ryhmät luotu</td>
          <td style={{"min-width": "22em"}}>
            <img 
              src={menu_white}
              alt=""
              className="d-inline-block align-text-top"
              width="20"
              height="20"
            />
            Toiminnot
          </td>
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