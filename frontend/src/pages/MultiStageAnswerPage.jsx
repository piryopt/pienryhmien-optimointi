import { useState, useEffect, useRef } from "react";
import { DragDropContext } from "@hello-pangea/dnd";
import { useParams } from "react-router-dom";
import { useNotification } from "../context/NotificationContext.jsx";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys.js";
import Nav from "react-bootstrap/Nav";
import Tab from "react-bootstrap/Tab";
import Form from "react-bootstrap/Form";
import GroupList from "../components/survey_answer_page_components/GroupList.jsx";
import ReasonsBox from "../components/survey_answer_page_components/ReasonsBox.jsx";
import SurveyInfo from "../components/survey_answer_page_components/SurveyInfo.jsx";
import "../static/css/answerPage.css";
import { imagesBaseUrl } from "../utils/constants.js";
import ClosedMultistageSurveyView from "../components/survey_answer_page_components/ClosedMultistageSurveyView.jsx";
import ButtonRow from "../components/survey_answer_page_components/ButtonRow.jsx";
import GroupSearch from "../components/GroupSearch.jsx";

const MultiStageAnswerPage = () => {
  const { surveyId } = useParams();
  const { showNotification } = useNotification();
  const { t } = useTranslation();

  const [stages, setStages] = useState([]);
  const [survey, setSurvey] = useState({});
  const [loading, setLoading] = useState(true);
  const [expandedIds, setExpandedIds] = useState(new Set());
  const [reasons, setReasons] = useState({});
  const [additionalInfo, setAdditionalInfo] = useState(false);
  const [activeStage, setActiveStage] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [existing, setExisting] = useState(false);
  const mountedRef = useRef(false);

  useEffect(() => {
    mountedRef.current = true;

    (async () => {
      try {
        const data = await surveyService.getMultiStageSurvey(surveyId);
        if (!mountedRef.current) return;

        const stagesData = [];
        const initialReasons = {};

        for (const stage of data.stages || []) {
          const stageId = stage.name;
          let choices = stage.choices || [];
          /* Choice types in a survey:
            - Neutral: Not ordered
            - Good: Choices placed in green box
            - Bad: Choices placed in red box
          */
          let neutralChoices = [...choices];
          let goodChoices = [];
          let badChoices = [];

          if (data.existing === "1") {
            setExisting(true);
            const goodIds = (data.rankedStages[stageId]?.goodChoices || []).map(
              String
            );
            const badIds = (data.rankedStages[stageId]?.badChoices || []).map(
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

          stagesData.push({
            id: stageId,
            name: stage.name,
            neutral: neutralChoices,
            good: goodChoices,
            bad: badChoices,
            notAvailable: !!data.rankedStages?.[stageId]?.notAvailable,
            hasMandatory: stage.hasMandatory
          });
          initialReasons[stageId] = data.rankedStages?.[stageId]["reason"];
        }
        setStages(stagesData);
        setReasons(initialReasons);
        setAdditionalInfo(data.survey.additionalInfo || false);
        setSurvey(data.survey || {});
        setActiveStage(stagesData[0]?.id || null);
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
    const sourceParts = source.droppableId.split(/-(?=[^ -]+$)/);
    const sourceStage = sourceParts.length === 2 ? sourceParts[0] : "single";
    const sourceListId =
      sourceParts.length === 2 ? sourceParts[1] : sourceParts[0];

    const destParts = destination.droppableId.split(/-(?=[^ -]+$)/);
    const destStage = destParts.length === 2 ? destParts[0] : "single";
    const destListId = destParts.length === 2 ? destParts[1] : destParts[0];
    const stageIndex = stages.findIndex((s) => s.id === sourceStage);
    if (stageIndex === -1) return;
    const stage = stages[stageIndex];
    const sourceList = [...(stage[sourceListId] || [])];
    const destList =
      sourceStage === destStage && sourceListId === destListId
        ? sourceList
        : [...(stages.find((s) => s.id === destStage)?.[destListId] || [])];
    const [moved] = sourceList.splice(source.index, 1);
    if (!(sourceStage === destStage && sourceListId === destListId)) {
      ["good", "bad", "neutral"].forEach((listId) => {
        if (listId !== destListId) {
          stage[listId] = (stage[listId] || []).filter(
            (x) => x.id !== moved.id
          );
        }
      });
    }
    destList.splice(destination.index, 0, moved);
    setStages((prev) =>
      prev.map((s) =>
        s.id === stage.id
          ? { ...s, [sourceListId]: sourceList, [destListId]: destList }
          : s
      )
    );
  };

  // Additional information per item
  const toggleExpand = (itemId) => {
    setExpandedIds((prev) => {
      const next = new Set(prev);
      const id = itemId.toString();
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  // Marked as absent for current stage
  const toggleNotAvailable = (stageId) => {
    setStages((prev) =>
      prev.map((s) =>
        s.id === stageId ? { ...s, notAvailable: !s.notAvailable } : s
      )
    );
  };

  const handleSubmit = async () => {
    try {
      const payload = stages.map((s) => {
        if (s.notAvailable) {
          const allIds = [
            ...(s.neutral || []),
            ...(s.good || []),
            ...(s.bad || [])
          ].map((c) => c.id);
          return {
            stageId: s.id,
            notAvailable: true,
            good: [],
            bad: [],
            neutral: allIds,
            reason: reasons[s.id]
          };
        }
        return {
          stageId: s.id,
          notAvailable: s.notAvailable,
          good: s.good.map((c) => c.id),
          bad: s.bad.map((c) => c.id),
          neutral: s.neutral.map((c) => c.id),
          reason: reasons[s.id]
        };
      });

      for (const stage of stages) {
        if (stage.notAvailable) continue;

        if (
          survey.denied_allowed_choices === 0
            ? stage.good.length < survey.min_choices_per_stage[stage.name]
            : stage.good.length + stage.bad.length <
              survey.min_choices_per_stage[stage.name]
        ) {
          showNotification(
            t(
              "Sijoita vähintään {{min}} ryhmää jokaisesta vaiheesta vihreään tai punaiseen laatikkoon {{absence}}",
              {
                min: survey.min_choices_per_stage[stage.name],
                absence: survey.allow_absences
                  ? t("tai merkitse itsesi poissaolevaksi vaiheesta")
                  : ""
              }
            ),
            "error"
          );
          return;
        }

        if (stage.bad.length > survey.denied_allowed_choices) {
          showNotification(
            t(
              "Voit kieltää enintään {{max}} jokaisesta vaiheesta",
              {
                max: survey.denied_allowed_choices
              }
            ),
            "error"
          );
          return;
        }

        if (stage.bad.length > 0 && (reasons[stage.name]?.length ?? 0) < 10) {
          showNotification(
            t(
              "Vaiheen {{name}} kieltojen perustelun tulee olla vähintään 10 merkkiä pitkä",
              {
                name: stage.name
              }
            ),
            "error"
          );
          return;
        }
      }
      const result = await surveyService.submitMultiStageAnswers({
        surveyId,
        minChoices: survey.min_choices,
        deniedAllowedChoices: survey.denied_allowed_choices,
        stages: payload
      });
      setExisting(true);
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

  const handleDelete = async () => {
    try {
      const result = await surveyService.deleteSurveyAnswer(surveyId);
      if (result.status === "0") throw new Error(result.msg);
      showNotification(t(result.msg), "success");
      setStages((prev) =>
        prev.map((s) => ({
          ...s,
          good: [],
          bad: [],
          neutral: [...s.good, ...s.bad, ...s.neutral],
          notAvailable: false
        }))
      );
      setReasons({});
      setExisting(false);
    } catch (error) {
      showNotification(t(error.message), "error");
      console.error("Error deleting survey", error);
    }
  };

  const indexOfCurrStage = () => {
    return stages.findIndex((stage) => stage.name === activeStage);
  };
  const currentStage = stages[indexOfCurrStage()] || null;
  if (loading)
    return <div className="text-center mt-5">{t("Ladataan kyselyä...")}</div>;
  if (!activeStage) return <div>{t("Ei vaiheita ladattuna")}</div>;

  if (survey.closed)
    return (
      <div className="answer-page">
        <h2 className="answer-title">
          <img
            src={`${imagesBaseUrl}/assignment_white_36dp.svg`}
            alt=""
            className="assignment-icon"
          />
          {survey.name}
        </h2>
        <ClosedMultistageSurveyView
          existing={existing}
          stages={stages}
          reasons={reasons}
          expandedIds={expandedIds}
          toggleExpand={toggleExpand}
        />
      </div>
    );

  return (
    <div className="answer-page">
      <div>
        <h2 className="answer-title">
          <img
            src={`${imagesBaseUrl}/assignment_white_36dp.svg`}
            alt=""
            className="assignment-icon"
          />
          {survey.name}
        </h2>
        <SurveyInfo
          survey={survey}
          additionalInfo={additionalInfo}
          choices={[
            ...stages[indexOfCurrStage()].neutral,
            ...stages[indexOfCurrStage()].bad,
            ...stages[indexOfCurrStage()].good
          ]}
          stageName={currentStage?.name || null}
        />
      </div>

      <DragDropContext onDragEnd={handleDragEnd}>
        <Tab.Container activeKey={activeStage} onSelect={setActiveStage}>
          <Nav variant="tabs" className="mb-3 justify-content-center">
            {stages.map(({ id, name, notAvailable }) => (
              <Nav.Item key={id}>
                <Nav.Link eventKey={id}>
                  {name}
                  {notAvailable ? ` (${t("poissa")})` : ""}
                </Nav.Link>
              </Nav.Item>
            ))}
          </Nav>

          <Tab.Content>
            {stages.map((stage) => (
              <Tab.Pane key={stage.id} eventKey={stage.id}>
                <div className="stage-section">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <h3 className="stage-title">{stage.name}</h3>
                    {survey.allow_absences && (
                      <Form.Check
                        type="switch"
                        id={`not-available-${stage.id}`}
                        label={t("En ole paikalla tässä vaiheessa")}
                        checked={stage.notAvailable}
                        onChange={() => toggleNotAvailable(stage.id)}
                      />
                    )}
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
                    {t(
                      `Järjestä vaihtoehdot mieluisuusjärjestykseen${
                        survey.allow_absences
                          ? " tai merkitse itsesi poissaolevaksi."
                          : "."
                      }`
                    )}
                  </p>
                  {stage.hasMandatory && !stage.notAvailable && (
                    <p className="note">
                      {t("HUOM! ")}
                      <span className="mandatory">{t("Pakolliseksi ")}</span>
                      {t(
                        "merkityt ryhmät priorisoidaan jakamisprosessissa. "
                      )}{" "}
                      {t(
                        "Ne täytetään aina vähintään minimikokoon asti vastauksista riippumatta."
                      )}
                      <br />
                      {(survey.denied_allowed_choices ?? 0) !== 0 && (
                        <>
                          {t("Sinut voidaan tarvittaessa sijoittaa")}{" "}
                          <span className="mandatory">{t("pakolliseen")}</span>{" "}
                          {t("ryhmään, vaikka olisitkin kieltänyt sen.")}
                        </>
                      )}
                    </p>
                  )}

                  {!stage.notAvailable ? (
                    <div className="answer-layout">
                      <div className="left-column">
                        <GroupList
                          id={`${stage.id}-good`}
                          items={stage.good}
                          expandedIds={expandedIds}
                          toggleExpand={toggleExpand}
                          choices={stage.neutral}
                          stageId={stage.id}
                          multiphase={true}
                        />
                        {(survey.denied_allowed_choices ?? 0) !== 0 && (
                          <>
                            <GroupList
                              id={`${stage.id}-bad`}
                              items={stage.bad}
                              expandedIds={expandedIds}
                              toggleExpand={toggleExpand}
                              choices={stage.neutral}
                              stageId={stage.id}
                              multiphase={true}
                            />
                            <ReasonsBox
                              key={stage.id}
                              reason={reasons[stage.id] || ""}
                              setReason={(value) =>
                                setReasons({ ...reasons, [stage.id]: value })
                              }
                            />
                          </>
                        )}
                        <ButtonRow
                          handleSubmit={handleSubmit}
                          handleDelete={handleDelete}
                          existing={existing}
                        />
                      </div>
                      <div className="right-column">
                        <GroupSearch
                          searchTerm={searchTerm}
                          setSearchTerm={setSearchTerm}
                        />
                        <GroupList
                          id={`${stage.id}-neutral`}
                          items={stage.neutral}
                          expandedIds={expandedIds}
                          toggleExpand={toggleExpand}
                          choices={stage.neutral}
                          stageId={stage.id}
                          multiphase={true}
                          searchTerm={searchTerm}
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
                      {t("Olet ilmoittautunut poissaolevaksi.")}
                      <div className="submit-row mt-4">
                        <ButtonRow
                          handleSubmit={handleSubmit}
                          handleDelete={handleDelete}
                          existing={existing}
                        />
                      </div>
                    </div>
                  )}
                </div>
              </Tab.Pane>
            ))}
          </Tab.Content>
        </Tab.Container>
      </DragDropContext>
    </div>
  );
};

export default MultiStageAnswerPage;
