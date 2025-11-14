const SurveyInfo = ({ survey, additionalInfo }) => (
  <>
    <p className="deadline">Vastausaika päättyy {survey.deadline}</p>
    <p style={{ padding: "1.5em 0" }}>{survey.description}</p>
    <p className="instructions">
      <i>
        Raahaa oikean reunan listasta vähintään {survey.min_choices} vaihtoehtoa
        <span className="highlight"> vihreään</span> laatikkoon.
      </i>
      {additionalInfo ? (
        <i> Klikkaa valintavaihtoehtoa nähdäksesi siitä lisätietoa.</i>
      ) : null}
    </p>
  </>
);

export default SurveyInfo;
