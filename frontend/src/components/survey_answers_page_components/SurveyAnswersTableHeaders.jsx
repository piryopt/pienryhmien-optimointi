import { useTranslation } from "react-i18next";
import emailWhite from "/images/email_white_36dp.svg";
import doneWhite from "/images/done_white_36dp.svg";
import questionAnswerWhite from "/images/question_answer_white_36dp.svg";
import personOffWhite from "/images/person_off_white_36dp.svg";

const SurveyAnswersTableHeaders = () => {
  const { t } = useTranslation();

  return (
    <tr>
      <th>
        <img
          src={emailWhite}
          alt=""
          width={24}
          height={24}
          className="d-inline-block align-text-top"
        />
        &nbsp;{t("Sähköposti")}
      </th>
      <th style={{ minWidth: "12em" }}>
        <img
          src={doneWhite}
          alt=""
          width={24}
          height={24}
          className="d-inline-block align-text-top"
        />
        &nbsp;{t("Valinnat")}
      </th>
      <th>
        <img
          src={questionAnswerWhite}
          alt=""
          width={24}
          height={24}
          className="d-inline-block align-text-top"
        />
        &nbsp;{t("Perustelut")}
      </th>
      <th>
        <img
          src={personOffWhite}
          alt=""
          width={24}
          height={24}
          className="d-inline-block align-text-top"
        />
        &nbsp;{t("Vastauksen poistaminen")}
      </th>
    </tr>
  );
};

export default SurveyAnswersTableHeaders;
