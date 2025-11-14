import GroupList from "./GroupList.jsx";
import ClosedSurveyNotification from "./ClosedSurveyNotification.jsx";
import { useTranslation } from "react-i18next";

const ClosedSurveyView = ({
  good = [],
  bad = [],
  neutral = [],
  expandedIds,
  toggleExpand,
  reason,
  existing
}) => {
  const { t } = useTranslation();

  return (
    <>
      <div>
        <ClosedSurveyNotification existing={existing} />
      </div>

      <div className="answer-layout">
        <div className="left-column">
          {good.length > 0 && (
            <>
              <h2 className="closed-survey-title">{t("Valinnat")}:</h2>
              <GroupList
                id="good"
                items={good}
                expandedIds={expandedIds}
                toggleExpand={toggleExpand}
                choices={neutral}
                readOnly
              />
            </>
          )}
        </div>

        <div className="right-column" style={{ marginLeft: 15 }}>
          {bad.length > 0 && (
            <>
              <h2 className="closed-survey-title">{t("Hylkäykset")}:</h2>
              <GroupList
                id="bad"
                items={bad}
                expandedIds={expandedIds}
                toggleExpand={toggleExpand}
                choices={neutral}
                readOnly
              />
              {reason && reason.length > 0 ? (
                <div style={{ paddingLeft: 11 }}>
                  <p>
                    {t("Perustelut hylkäyksille")}:
                    <br /> {reason}
                  </p>
                </div>
              ) : null}
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default ClosedSurveyView;
