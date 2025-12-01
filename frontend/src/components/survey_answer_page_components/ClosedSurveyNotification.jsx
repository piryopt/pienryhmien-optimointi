import "../../static/css/answerPage.css";
import { imagesBaseUrl } from "../../utils/constants";
import { useTranslation } from "react-i18next";

const ClosedSurveyNotification = ({ existing }) => {
  const { t } = useTranslation();
  console.log("ClosedSurveyNotification existing:", existing);
  return (
    <div className="closed-survey-notifier">
      <div className="closed-survey-icon">
        <img
          src={`${imagesBaseUrl}/warning_amber_white_36dp.svg`}
          alt=""
          width="100%"
          height="100%"
          className="d-inline-block align-text-middle"
        />
      </div>
      <div className="closed-survey-content">
        <h2>{t("Kysely on suljettu")}</h2>
        <p>
          {" "}
          {t("Tämä kysely on suljettu eikä siihen voi enää vastata.")}
          {existing ? (
            <>
              {" "}
              {t(
                "Vastauksesi kyselyyn on talletettu ja näet tekemäsi valinnat alta."
              )}
            </>
          ) : (
            <> {t("Et ole vastannut tähän kyselyyn.")}</>
          )}
        </p>
      </div>
    </div>
  );
};

export default ClosedSurveyNotification;
