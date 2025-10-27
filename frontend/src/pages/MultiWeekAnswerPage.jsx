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
import "../static/css/answerPage.css";

const MultiWeekAnswerPage = () => {
  const { surveyId } = useParams();
  const { showNotification } = useNotification();
  const { t } = useTranslation();

  const [weeks, setWeeks] = useState({});
  const [survey, setSurvey] = useState({});
  const [loading, setLoading] = useState(true);
  const [expandedIds, setExpandedIds] = useState(new Set());
  const [reason, setReason] = useState("");
  const [additionalInfo, setAdditionalInfo] = useState(false);
  const [activeWeek, setActiveWeek] = useState(null);
  const mountedRef = useRef(false);

  useEffect(() => {
    mountedRef.current = true;

    (async () => {
      try {
        const data = {
          survey: {
            id: "123",
            name: "Kurssivalinnat keväälle 2025",
            deadline: "31.10.2025",
            min_choices: 2,
            denied_allowed_choices: 1
          },
          reason: "",
          additional_info: true,
          weeks: [
            {
              id: "1",
              name: "Viikko 1",
              existing: "0",
              choices: [
                {
                  id: "a1",
                  name: "Ohjelmointi 1",
                  mandatory: false,
                  description: "Johdatus ohjelmointiin."
                },
                {
                  id: "a2",
                  name: "Matematiikka 1",
                  mandatory: true,
                  description: "Perusmatematiikkaa insinööreille."
                },
                {
                  id: "a3",
                  name: "Englanti A",
                  mandatory: false,
                  description: "Akateemista englantia."
                }
              ],
              goodChoices: [],
              badChoices: []
            },
            {
              id: "2",
              name: "Viikko 2",
              existing: "0",
              choices: [
                {
                  id: "b1",
                  name: "Tietokannat",
                  mandatory: false,
                  description: "SQL ja relaatiomallit."
                },
                {
                  id: "b2",
                  name: "Ohjelmointi 2",
                  mandatory: false,
                  description: "Jatkokurssi ohjelmointiin."
                },
                {
                  id: "b3",
                  name: "Ruotsi B",
                  mandatory: false,
                  description: "Ruotsin kielen perusteet."
                }
              ],
              goodChoices: [],
              badChoices: []
            },
            {
              id: "3",
              name: "Viikko 3",
              existing: "1",
              choices: [
                {
                  id: "c1",
                  name: "Web-sovelluskehitys",
                  mandatory: false,
                  description: "React, Node.js ja REST-rajapinnat."
                },
                {
                  id: "c2",
                  name: "Tietoturva",
                  mandatory: true,
                  description: "Kyberturvallisuuden perusteet."
                },
                {
                  id: "c3",
                  name: "Projektityö",
                  mandatory: false,
                  description: "Ryhmätyö projektimuotoisesti."
                }
              ],
              goodChoices: [],
              badChoices: []
            }
          ]
        };

        if (!mountedRef.current) return;

        const weeksData = {};
        for (const week of data.weeks || []) {
          let neutralChoices = [...(week.choices || [])];
          let goodChoices = [];
          let badChoices = [];

          if (week.existing === "1") {
            const goodIds = new Set((week.goodChoices || []).map(String));
            const badIds = new Set((week.badChoices || []).map(String));

            goodChoices = week.choices.filter((c) => goodIds.has(String(c.id)));
            badChoices = week.choices.filter((c) => badIds.has(String(c.id)));

            const used = new Set(
              [...goodChoices, ...badChoices].map((c) => String(c.id))
            );
            neutralChoices = week.choices.filter(
              (c) => !used.has(String(c.id))
            );
          }

          weeksData[week.id] = {
            name: week.name || `Viikko ${week.id}`,
            neutral: neutralChoices,
            good: goodChoices,
            bad: badChoices,
            notAvailable: false
          };
        }

        setWeeks(weeksData);
        setSurvey(data.survey || {});
        setReason(data.reason || "");
        setAdditionalInfo(data.additional_info || false);
        setActiveWeek(Object.keys(weeksData)[0] || null);
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
    const sourceWeek = sourceParts.length === 2 ? sourceParts[0] : "single";
    const sourceListId =
      sourceParts.length === 2 ? sourceParts[1] : sourceParts[0];

    const destParts = destination.droppableId.split("-");
    const destWeek = destParts.length === 2 ? destParts[0] : "single";
    const destListId = destParts.length === 2 ? destParts[1] : destParts[0];

    if (!weeks[sourceWeek] || !weeks[destWeek]) return;

    const sourceList = [...(weeks[sourceWeek][sourceListId] || [])];
    const destList =
      sourceWeek === destWeek && sourceListId === destListId
        ? sourceList
        : [...(weeks[destWeek][destListId] || [])];

    const [moved] = sourceList.splice(source.index, 1);

    if (!(sourceWeek === destWeek && sourceListId === destListId)) {
      ["good", "bad", "neutral"].forEach((listId) => {
        if (listId !== destListId) {
          weeks[sourceWeek][listId] = (weeks[sourceWeek][listId] || []).filter(
            (x) => x.id !== moved.id
          );
        }
      });
    }

    destList.splice(destination.index, 0, moved);

    setWeeks((prev) => ({
      ...prev,
      [sourceWeek]: {
        ...prev[sourceWeek],
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

  const toggleNotAvailable = (weekId) => {
    setWeeks((prev) => ({
      ...prev,
      [weekId]: { ...prev[weekId], notAvailable: !prev[weekId].notAvailable }
    }));
  };

  const handleSubmit = async () => {
    try {
      const payload = Object.entries(weeks).map(([weekId, lists]) => ({
        weekId,
        notAvailable: lists.notAvailable,
        good: lists.good.map((c) => c.id),
        bad: lists.bad.map((c) => c.id),
        neutral: lists.neutral.map((c) => c.id)
      }));

      const result = await surveyService.submitMultiWeekAnswers({
        surveyId,
        weeks: payload,
        reason
      });

      if (result.status === "0") throw new Error(result.msg);
      showNotification(t(result.msg), "success");
    } catch (error) {
      console.error("Error submitting survey", error);
      showNotification(t(error.message), "error");
    }
  };

  if (loading)
    return <div className="text-center mt-5">Ladataan kyselyä...</div>;
  if (!activeWeek) return <div>Ei viikkoja ladattuna</div>;

  return (
    <div className="answer-page">
      <div>
        <h1 className="answer-title">
          <img src={assignmentIcon} alt="" className="assignment-icon" />
          {survey.name}
        </h1>
        <p className="deadline">Vastausaika päättyy {survey.deadline}</p>
        <p className="instructions">
          <i>
            Raahaa jokaiselta viikolta vähintään {survey.min_choices}{" "}
            vaihtoehtoa <span className="highlight">vihreään</span> laatikkoon.
          </i>
          {additionalInfo && (
            <i> Klikkaa valintavaihtoehtoa nähdäksesi lisätietoa.</i>
          )}
        </p>
      </div>

      <DragDropContext onDragEnd={handleDragEnd}>
        <Tab.Container activeKey={activeWeek} onSelect={setActiveWeek}>
          <Nav variant="tabs" className="mb-3 justify-content-center">
            {Object.entries(weeks).map(([weekId, { name, notAvailable }]) => (
              <Nav.Item key={weekId}>
                <Nav.Link eventKey={weekId}>
                  {name}
                  {notAvailable ? " (poissa)" : ""}
                </Nav.Link>
              </Nav.Item>
            ))}
          </Nav>

          <Tab.Content>
            {Object.entries(weeks).map(([weekId, week]) => (
              <Tab.Pane key={weekId} eventKey={weekId}>
                <div className="week-section">
                  <div className="d-flex justify-content-between align-items-center mb-2">
                    <h2 className="week-title">{week.name}</h2>
                    <Form.Check
                      type="switch"
                      id={`not-available-${weekId}`}
                      label="En ole paikalla tällä viikolla"
                      checked={week.notAvailable}
                      onChange={() => toggleNotAvailable(weekId)}
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

                  {!week.notAvailable ? (
                    <div className="answer-layout">
                      <div className="left-column">
                        <GroupList
                          id={`${weekId}-good`}
                          items={week.good}
                          expandedIds={expandedIds}
                          toggleExpand={toggleExpand}
                          choices={week.neutral}
                          weekId={weekId}
                          multiphase={true}
                        />
                        {(survey.denied_allowed_choices ?? 0) !== 0 && (
                          <GroupList
                            id={`${weekId}-bad`}
                            items={week.bad}
                            expandedIds={expandedIds}
                            toggleExpand={toggleExpand}
                            choices={week.neutral}
                            weekId={weekId}
                            multiphase={true}
                          />
                        )}
                      </div>

                      <div className="right-column">
                        <GroupList
                          id={`${weekId}-neutral`}
                          items={week.neutral}
                          expandedIds={expandedIds}
                          toggleExpand={toggleExpand}
                          choices={week.neutral}
                          weekId={weekId}
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
                      Olet ilmoittanut olevasi poissa tällä viikolla.
                    </div>
                  )}
                </div>
              </Tab.Pane>
            ))}
          </Tab.Content>
        </Tab.Container>
      </DragDropContext>

      {(survey.denied_allowed_choices ?? 0) !== 0 && (
        <ReasonsBox reason={reason} setReason={setReason} />
      )}

      <div className="submit-row mt-4">
        <Button variant="success" className="submit-btn" onClick={handleSubmit}>
          Lähetä kaikki viikkovalinnat
        </Button>
      </div>
    </div>
  );
};

export default MultiWeekAnswerPage;
