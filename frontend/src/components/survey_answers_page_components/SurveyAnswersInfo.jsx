import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

const SurveyAnswersInfo = ({ answersAmount, availableSpaces }) => {
  const { t } = useTranslation();
  return (
    <>
      <br />
      <i>
        {t("Vastauksia")}: {answersAmount}
      </i>
      <br />
      <i>
        {t("Jaettavia paikkoja")}: {availableSpaces}
      </i>
      <br />
      <br />
      <Link to="/surveys" className="surveys_link" style={{ float: "right" }}>
        {t("Palaa kyselylistaan")}
      </Link>
      <br />
      <br />
    </>
  );
};

export default SurveyAnswersInfo;
