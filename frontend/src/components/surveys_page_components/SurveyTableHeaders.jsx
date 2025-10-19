import { useTranslation } from "react-i18next";
import menuWhite from "/images/menu_white_36dp.svg";
import assignmentWhite from "/images/assignment_white_36dp.svg";
import toggleOnWhite from "/images/toggle_on_white_36dp.svg";
import toggleOffWhite from "/images/toggle_off_white_36dp.svg";
import scheduleWhite from "/images/schedule_white_36dp.svg";

const SurveyTableHeaders = () => {
  const { t } = useTranslation();

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
          &nbsp;{t("Kysely")}
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
          &nbsp;{t("Kyselyn tila")}
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
          &nbsp;{t("Ryhmät luotu")}
        </p>
      </th>
      <th style={{"minWidth": "22em"}}>
        <p>
          <img 
            src={menuWhite}
            alt=""
            className="d-inline-block align-text-top"
            width="24"
            height="24"
            />
          &nbsp;{t("Toiminnot")}
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
          &nbsp;{t("Vastausaika päättyy")}
        </p>
      </th>
    </tr>
  );
};

export default SurveyTableHeaders;