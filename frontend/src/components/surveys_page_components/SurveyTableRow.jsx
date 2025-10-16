import { useState } from "react";
import SurveyMoreInfo from "./SurveyMoreInfo";
import menu_white from "../../static/images/menu_white_36dp.svg";

const SurveyTableRow = ({ survey }) => {
  const [moreInfoVisible, setMoreInfoVisible] = useState(!survey.closed);

  return (
    <tr>
      <td>{survey.surveyname}</td>
      <td>
        <p style={{color: survey.closed ? "orangered" : "green"}}>
          {survey.closed ? "Suljettu" : "Avoin"}
        </p>
      </td>
      <td>
        <p style={{color: survey.results_saved && "green"}}>
          {survey.results_saved ? "Kyllä" : "Ei"}
        </p>
      </td>
      <td>
        <div 
          onClick={() => setMoreInfoVisible(!moreInfoVisible)}
          >
          <label style={{"cursor": "pointer"}} className="surveys_link">
            <img 
              src={menu_white}
              alt=""
              className="d-inline-block align-text-top"
              width="20"
              height="20"
            />
            &nbsp;
            {moreInfoVisible ? "Piilota" : "Näytä"}
          </label>
        </div>
        {moreInfoVisible && <SurveyMoreInfo survey={survey} />}
      </td>
      <td>{survey.time_end}</td>
    </tr>
  );
};

export default SurveyTableRow;