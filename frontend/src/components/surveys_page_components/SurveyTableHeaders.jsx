import menuWhite from "../../static/images/menu_white_36dp.svg";
import assignmentWhite from "../../static/images/assignment_white_36dp.svg";
import toggleOnWhite from "../../static/images/toggle_on_white_36dp.svg";
import toggleOffWhite from "../../static/images/toggle_off_white_36dp.svg";
import scheduleWhite from "../../static/images/schedule_white_36dp.svg";

const SurveyTableHeaders = () => {
  return (
    <tr>
      <td>
        <img 
          src={assignmentWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="24"
          height="24"
        />
        &nbsp;
        Kysely
      </td>
      <td>
        <img 
          src={toggleOnWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="24"
          height="24"
        />
        &nbsp;
        Kyselyn tila
      </td>
      <td>
        <img 
          src={toggleOffWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="24"
          height="24"
        />
        &nbsp;
        Ryhmät luotu
      </td>
      <td style={{"min-width": "22em"}}>
        <img 
          src={menuWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="24"
          height="24"
        />
        &nbsp;
        Toiminnot
      </td>
      <td>
        <img 
          src={scheduleWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="24"
          height="24"
        />
        &nbsp;
        Vastausaika päättyy
      </td>
    </tr>
  );
};

export default SurveyTableHeaders;