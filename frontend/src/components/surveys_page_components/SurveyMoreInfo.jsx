const SurveyMoreInfo = ({ survey }) => {
  return (
    <div>
      <a href={`surveys/${survey.id}/answers`}
          className="surveys_link">
          Tarkastele tuloksia
      </a>
      <br></br>
      <a className="surveys_link">
        Kopioi kyselyn osoite leikepöydälle
      </a>
    </div>
  )
};

export default SurveyMoreInfo;