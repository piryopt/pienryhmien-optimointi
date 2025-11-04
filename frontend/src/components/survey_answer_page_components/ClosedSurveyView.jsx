import GroupList from "./GroupList.jsx";
import ClosedSurveyNotification from "./ClosedSurveyNotification.jsx";

const ClosedSurveyView = ({
  good = [],
  bad = [],
  neutral = [],
  expandedIds,
  toggleExpand,
  reason,
  existing
}) => {
  return (
    <>
      <div>
        <ClosedSurveyNotification existing={existing} />
      </div>

      <div className="answer-layout">
        <div className="left-column">
          {good.length > 0 && (
            <>
              <h2 className="closed-survey-title">Valinnat</h2>
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
              <h2 className="closed-survey-title">Hylkäykset</h2>
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
                    Perustelut hylkäyksille:
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
