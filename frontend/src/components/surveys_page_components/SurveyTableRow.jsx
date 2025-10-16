import { useState } from "react";
import SurveyMoreInfo from "./SurveyMoreInfo";
import menu_white from "../../static/images/menu_white_36dp.svg";

const SurveyTableRow = ({ survey }) => {
  const [moreInfoVisible, setMoreInfoVisible] = useState(false);

  return (
    <tr>
      <td>{survey.surveyname}</td>
      <td>{survey.closed ? "Suljettu" : "Avoin"}</td>
      <td>{survey.results_saved ? "Kyllä" : "Ei"}</td>
      <td>
        <div 
          id={`closed_more_info_container_${survey.id}`}
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