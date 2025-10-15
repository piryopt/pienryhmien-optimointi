const SurveysTable = ({ activeSurveys, closedSurveys}) => (
  <table className="table table-striped">
    <thead className="table-dark">
      <tr>
        <td>Kysely</td>
        <td>Kyselyn tila</td>
        <td>Ryhmät luotu</td>
        <td>Toiminnot</td>
        <td>Vastausaika päättyy</td>
      </tr>
    </thead>
    <tbody>
      {activeSurveys.map((survey, i) => 
        <tr key={i}>
          <td>{survey.surveyname}</td>
          <td>{survey.closed ? "Suljettu" : "Avoin"}</td>
          <td>{survey.results_saved ? "Kyllä" : "Ei"}</td>
          <td>Näytä XD</td>
          <td>{survey.time_end}</td>
        </tr>
      )}
      <tr>
        <td>---</td>
        <td>---</td>
        <td>---</td>
        <td>---</td>
        <td>---</td>
      </tr>
      {closedSurveys.map((survey, i) => 
        <tr key={i}>
          <td>{survey.surveyname}</td>
          <td>{survey.closed ? "Suljettu" : "Avoin"}</td>
          <td>{survey.results_saved ? "Kyllä" : "Ei"}</td>
          <td>Näytä XD</td>
          <td>{survey.time_end}</td>
        </tr>
      )}
    </tbody>
  </table>
);

export default SurveysTable;