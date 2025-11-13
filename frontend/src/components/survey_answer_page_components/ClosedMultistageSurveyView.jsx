import GroupList from "./GroupList.jsx";
import ClosedSurveyNotification from "./ClosedSurveyNotification.jsx";
import StageDropdown from "./../survey_answers_page_components/StageDropdown.jsx";
import { useEffect, useState } from "react";

const ClosedMultistageSurveyView = ({
  stages,
  reasons,
  existing,
  expandedIds,
  toggleExpand
}) => {
  // derive labels for dropdown from stage objects (prefer human label 'stage' if present)
  const stageLabels = (stages || []).map((s) => s.stage ?? s.id);
  const [currStage, setCurrStage] = useState(stageLabels.length > 0 ? stageLabels[0] : "");

  // keep current stage in sync when stages prop changes
  useEffect(() => {
    const labels = (stages || []).map((s) => s.stage ?? s.id);
    if (!labels.includes(currStage)) {
      setCurrStage(labels[0] ?? "");
    }
  }, [stages]);

  return (
    <>
      <div>
        <ClosedSurveyNotification existing={existing} />
      </div>

      {existing && stageLabels.length > 0 && (
        <div style={{ margin: "0 0 1rem 0" }}>
          <StageDropdown
            stages={stageLabels}
            currStage={currStage}
            setCurrStage={setCurrStage}
          />
        </div>
      )}

      {existing && (
        <>
          {stages
            .filter((stage) => (stage.stage ?? stage.id) === currStage)
            .map((stage) => (
              <div className="answer-layout" key={stage.id}>
                <div className="left-column">
                  {stage.good.length > 0 && (
                    <>
                      <h2 className="closed-survey-title">Valinnat:</h2>
                      <GroupList
                        id="good"
                        items={stage.good}
                        expandedIds={expandedIds}
                        toggleExpand={toggleExpand}
                        choices={stage.neutral}
                        readOnly={true}
                      />
                    </>
                  )}
                </div>

                <div className="right-column" style={{ marginLeft: 15 }}>
                  {stage.bad.length > 0 && (
                    <>
                      <h2 className="closed-survey-title">Hylkäykset:</h2>
                      <GroupList
                        id="bad"
                        items={stage.bad}
                        expandedIds={expandedIds}
                        toggleExpand={toggleExpand}
                        choices={stage.neutral}
                        readOnly={true}
                      />
                      {reasons[stage.id] && reasons[stage.id].length > 0 ? (
                        <div style={{ paddingLeft: 11 }}>
                          <p>
                            Perustelut hylkäyksille:
                            <br /> {reasons[stage.id]}
                          </p>
                        </div>
                      ) : null}
                    </>
                  )}
                </div>
              </div>
            ))}
        </>
      )}
    </>
  );
};

export default ClosedMultistageSurveyView;
