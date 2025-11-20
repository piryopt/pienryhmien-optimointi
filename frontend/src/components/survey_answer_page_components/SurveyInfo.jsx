const SurveyInfo = ({ survey, additionalInfo, choices, stageName = null }) => {
  const min_choices = !stageName
    ? Number(survey.min_choices)
    : Number(survey.min_choices_per_stage[stageName]);
  const a_d_c = Number(survey.denied_allowed_choices);
  const total = choices.length;
  console.log("current stage choices:", choices);

  const isAll = total > 0 && min_choices === total;
  const denySome = a_d_c > 0;

  return (
    <>
      <p className="deadline">Vastausaika päättyy {survey.deadline}</p>
      <p style={{ padding: "1.5em 0" }}>{survey.description}</p>

      <p className="instructions">
        <i>
          {isAll && !denySome && (
            <>
              Raahaa kaikki vaihtoehdot{" "}
              <span className="highlight-green">vihreään</span> laatikkoon.
            </>
          )}

          {isAll && denySome && (
            <>
              Raahaa kaikki vaihtoehdot{" "}
              <span className="highlight-green">vihreään</span> tai{" "}
              <span className="highlight-red">punaiseen</span> laatikkoon.
              <br />
              <span>
                Voit kieltää {a_d_c} vaihtoehtoa{" "}
                <span className="highlight-red">punaiseen</span> laatikkoon.
              </span>
            </>
          )}

          {!isAll && !denySome && (
            <>
              Raahaa ainakin {min_choices} vaihtoehtoa{" "}
              <span className="highlight-green">vihreään</span> laatikkoon.
            </>
          )}

          {!isAll && denySome && (
            <>
              Raahaa ainakin {min_choices} vaihtoehtoa{" "}
              <span className="highlight-green">vihreään</span> tai{" "}
              <span className="highlight-red">punaiseen</span> laatikkoon.
              <br />
              <span>
                Voit kieltää {a_d_c} vaihtoehtoa{" "}
                <span className="highlight-red">punaiseen</span> laatikkoon.
              </span>
            </>
          )}
        </i>

        {additionalInfo ? (
          <i> Klikkaa valintavaihtoehtoa nähdäksesi siitä lisätietoa.</i>
        ) : null}
      </p>
    </>
  );
};

export default SurveyInfo;
