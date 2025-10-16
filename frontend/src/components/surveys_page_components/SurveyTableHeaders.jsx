import menuWhite from "../../static/images/menu_white_36dp.svg";
import assignmentWhite from "../../static/images/assignment_white_36dp.svg";
import toggleOnWhite from "../../static/images/toggle_on_white_36dp.svg";
import toggleOffWhite from "../../static/images/toggle_off_white_36dp.svg";
import scheduleWhite from "../../static/images/schedule_white_36dp.svg";

const SurveyTableHeaders = () => {
  return (
    <tr>
      <th>
        <p>
          <img 
            src={assignmentWhite}
            alt=""
            className="d-inline-block align-text-top"
            width="24"
            height="24"
          />
          &nbsp;
          Kysely
        </p>
      </th>
      <th>
        <p>
          <img 
            src={toggleOnWhite}
            alt=""
            className="d-inline-block align-text-top"
            width="24"
            height="24"
          />
          &nbsp;
          Kyselyn tila
        </p>
      </th>
      <th>
        <p>
          <img 
            src={toggleOffWhite}
            alt=""
            className="d-inline-block align-text-top"
            width="24"
            height="24"
          />
          &nbsp;
          Ryhmät luotu
        </p>
      </th>
      <th style={{"min-width": "22em"}}>
        <p>
          <img 
            src={menuWhite}
            alt=""
            className="d-inline-block align-text-top"
            width="24"
            height="24"
            />
          &nbsp;
          Toiminnot
        </p>
      </th>
      <th>
        <p>
          <img 
            src={scheduleWhite}
            alt=""
            className="d-inline-block align-text-top"
            width="24"
            height="24"
          />
          &nbsp;
          Vastausaika päättyy
        </p>
      </th>
    </tr>
  );
};

export default SurveyTableHeaders;