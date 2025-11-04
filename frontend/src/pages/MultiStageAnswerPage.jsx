import { useState, useEffect, useRef } from "react";
import { DragDropContext } from "@hello-pangea/dnd";
import { useParams } from "react-router-dom";
import { useNotification } from "../context/NotificationContext.jsx";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys.js";
import Button from "react-bootstrap/Button";
import Nav from "react-bootstrap/Nav";
import Tab from "react-bootstrap/Tab";
import Form from "react-bootstrap/Form";
import GroupList from "../components/survey_answer_page_components/GroupList.jsx";
import ReasonsBox from "../components/survey_answer_page_components/ReasonsBox.jsx";
import assignmentIcon from "/images/assignment_white_36dp.svg";
import SurveyInfo from "../components/survey_answer_page_components/SurveyInfo.jsx";
import "../static/css/answerPage.css";

const MultiStageAnswerPage = () => {
  const { surveyId } = useParams();
  const { showNotification } = useNotification();
  const { t } = useTranslation();

  const [stages, setStages] = useState({});
  const [survey, setSurvey] = useState({});
  const [loading, setLoading] = useState(true);
  const [expandedIds, setExpandedIds] = useState(new Set());
  const [reasons, setReasons] = useState({});
  const [additionalInfo, setAdditionalInfo] = useState(false);
  const [activeStage, setActiveStage] = useState(null);
  const mountedRef = useRef(false);

  useEffect(() => {
    mountedRef.current = true;

    (async () => {
      try {
        const data = await surveyService.getMultiStageSurvey(surveyId);
        if (!mountedRef.current) return;

        const stagesData = {};
        const initialReasons = {};

        for (const [stageId, stage] of Object.entries(data.stages || {})) {
          const choices = stage.choices || [];
          let neutralChoices = [...choices];
          let goodChoices = [];
          let badChoices = [];
          if (data.existing === "1") {
            const goodIds = (data.rankedStages[stageId].goodChoices || []).map(
              String
            );
            const badIds = (data.rankedStages[stageId].badChoices || []).map(
              String
            );

            goodChoices = goodIds
              .map((id) => choices.find((c) => String(c.id) === id))
              .filter(Boolean);

            badChoices = badIds
              .map((id) => choices.find((c) => String(c.id) === id))
              .filter(Boolean);

            const usedIds = new Set([...goodIds, ...badIds]);
            neutralChoices = choices.filter((c) => !usedIds.has(String(c.id)));
          }

          stagesData[stageId] = {
            name: stageId,
            neutral: neutralChoices,
            good: goodChoices,
            bad: badChoices,
            notAvailable: !!data.rankedStages?.[stageId]?.notAvailable,
            hasMandatory: stage.hasMandatory
          };
        }

        setStages(stagesData);
        setReasons(initialReasons);
        setAdditionalInfo(data.survey.additionalInfo || false);
        setSurvey(data.survey || {});
        setActiveStage(Object.keys(stagesData)[0] || null);
      } catch (err) {
        console.error(err);
      } finally {
        if (mountedRef.current) setLoading(false);
      }
    })();

    return () => {
      mountedRef.current = false;
    };
  }, [surveyId]);

  const handleDragEnd = (result) => {
    const { source, destination } = result;
    if (!destination) return;

    const sourceParts = source.droppableId.split("-");
    const sourceStage = sourceParts.length === 2 ? sourceParts[0] : "single";
    const sourceListId =
      sourceParts.length === 2 ? sourceParts[1] : sourceParts[0];

    const destParts = destination.droppableId.split("-");
    const destStage = destParts.length === 2 ? destParts[0] : "single";
    const destListId = destParts.length === 2 ? destParts[1] : destParts[0];

    if (!stages[sourceStage] || !stages[destStage]) return;

    const sourceList = [...(stages[sourceStage][sourceListId] || [])];
    const destList =
      sourceStage === destStage && sourceListId === destListId
        ? sourceList
        : [...(stages[destStage][destListId] || [])];

    const [moved] = sourceList.splice(source.index, 1);

    if (!(sourceStage === destStage && sourceListId === destListId)) {
      ["good", "bad", "neutral"].forEach((listId) => {
        if (listId !== destListId) {
          stages[sourceStage][listId] = (
            stages[sourceStage][listId] || []
          ).filter((x) => x.id !== moved.id);
        }
      });
    }

    destList.splice(destination.index, 0, moved);

    setStages((prev) => ({
      ...prev,
      [sourceStage]: {
        ...prev[sourceStage],
        [sourceListId]: sourceList,
        [destListId]: destList
      }
    }));
  };

  const toggleExpand = (itemId) => {
    setExpandedIds((prev) => {
      const next = new Set(prev);
      const id = itemId.toString();
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const toggleNotAvailable = (stageId) => {
    setStages((prev) => ({
      ...prev,
      [stageId]: { ...prev[stageId], notAvailable: !prev[stageId].notAvailable }
    }));
  };

  const handleSubmit = async () => {
    try {
      const payload = Object.entries(stages).map(([stageId, lists]) => ({
        stageId,
        notAvailable: lists.notAvailable,
        good: lists.good.map((c) => c.id),
        bad: lists.bad.map((c) => c.id),
        neutral: lists.neutral.map((c) => c.id),
        reason: reasons[stageId]
      }));

      const result = await surveyService.submitMultiStageAnswers({
        surveyId,
        minChoices: survey.min_choices,
        deniedAllowedChoices: survey.denied_allowed_choices,
        stages: payload
      });
      if (result.status === "0") throw new Error(result.msg);
      showNotification(t("Kyselyn vastaukset tallennettu."), "success");
    } catch (error) {
      console.error("Error submitting survey", error);
      showNotification(
        t("Kyselyn vastauksien tallennus epäonnistui."),
        "error"
      );
    }
  };

  if (loading)
    return <div className="text-center mt-5">Ladataan kyselyä...</div>;
  if (!activeStage) return <div>Ei vaiheita ladattuna</div>;

  return (
    <div className="answer-page">
      <div>
        <h2 className="answer-title">
          <img src={assignmentIcon} alt="" className="assignment-icon" />
          {survey.name}
        </h2>
        <SurveyInfo survey={survey} additionalInfo={additionalInfo} />
      </div>

      <DragDropContext onDragEnd={handleDragEnd}>
        <Tab.Container activeKey={activeStage} onSelect={setActiveStage}>
          <Nav variant="tabs" className="mb-3 justify-content-center">
            {Object.entries(stages).map(([stageId, { name, notAvailable }]) => (
              <Nav.Item key={stageId}>
                <Nav.Link eventKey={stageId}>
                  {name}
                  {notAvailable ? " (poissa)" : ""}
                </Nav.Link>
              </Nav.Item>
            ))}
          </Nav>

          <Tab.Content>
            {Object.entries(stages).map(([stageId, stage]) => (
              <Tab.Pane key={stageId} eventKey={stageId}>
                <div className="stage-section">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <h3 className="stage-title">{stage.name}</h3>
                    <Form.Check
                      type="switch"
                      id={`not-available-${stageId}`}
                      label="En ole paikalla tässä vaiheessa"
                      checked={stage.notAvailable}
                      onChange={() => toggleNotAvailable(stageId)}
                    />
                  </div>
                  <p
                    style={{
                      fontStyle: "italic",
                      opacity: 0.8,
                      fontSize: "0.95rem",
                      marginTop: "-4px",
                      marginBottom: "1.2rem"
                    }}
                  >
                    Järjestä vaihtoehdot mieluisuusjärjestykseen tai merkitse
                    itsesi poissaolevaksi.
                  </p>
                  {stage.hasMandatory && !stage.notAvailable && (
                    <p className="note">
                      HUOM! <span className="mandatory">{"Pakolliseksi"}</span>{" "}
                      merkityt ryhmät priorisoidaan jakamisprosessissa. Ne
                      täytetään aina vähintään minimikokoon asti vastauksista
                      riippumatta.
                    </p>
                  )}

                  {!stage.notAvailable ? (
                    <div className="answer-layout">
                      <div className="left-column">
                        <GroupList
                          id={`${stageId}-good`}
                          items={stage.good}
                          expandedIds={expandedIds}
                          toggleExpand={toggleExpand}
                          choices={stage.neutral}
                          stageId={stageId}
                          multiphase={true}
                        />
                        {(survey.denied_allowed_choices ?? 0) !== 0 && (
                          <GroupList
                            id={`${stageId}-bad`}
                            items={stage.bad}
                            expandedIds={expandedIds}
                            toggleExpand={toggleExpand}
                            choices={stage.neutral}
                            stageId={stageId}
                            multiphase={true}
                          />
                        )}
                      </div>

                      <div className="right-column">
                        <GroupList
                          id={`${stageId}-neutral`}
                          items={stage.neutral}
                          expandedIds={expandedIds}
                          toggleExpand={toggleExpand}
                          choices={stage.neutral}
                          stageId={stageId}
                          multiphase={true}
                        />
                      </div>
                    </div>
                  ) : (
                    <div
                      style={{
                        color: "#aaa",
                        fontStyle: "italic",
                        margin: "3em 0"
                      }}
                    >
                      Olet ilmoittanut olevasi poissa tässä vaiheessa.
                    </div>
                  )}
                </div>
                {(survey.denied_allowed_choices ?? 0) !== 0 && (
                  <ReasonsBox
                    key={stageId}
                    reason={reasons[stageId] || ""}
                    setReason={(value) =>
                      setReasons({ ...reasons, [stageId]: value })
                    }
                  />
                )}
              </Tab.Pane>
            ))}
          </Tab.Content>
        </Tab.Container>
      </DragDropContext>

      <div className="submit-row mt-4">
        <Button variant="success" className="submit-btn" onClick={handleSubmit}>
          Lähetä kaikki valinnat
        </Button>
      </div>
    </div>
  );
};

export default MultiStageAnswerPage;
