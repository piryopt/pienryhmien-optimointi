import { useState, useEffect, useRef } from "react";
import { useParams } from "react-router-dom";
import { useNotification } from "../context/NotificationContext.jsx";
import surveyService from '../services/surveys.js';
import Header from '../components/survey_answer_page_components/Header.jsx';
import '../static/css/answerPage.css'; 
import ClosedSurveyView from "../components/survey_answer_page_components/ClosedSurveyView.jsx";
import SurveyInfo from "../components/survey_answer_page_components/SurveyInfo.jsx";
import { DragDropContext } from "@hello-pangea/dnd";
import { ReactReduxContext } from "react-redux";
import GroupList from '../components/survey_answer_page_components/GroupList.jsx';
import ReasonsBox from '../components/survey_answer_page_components/ReasonsBox.jsx';
import ButtonRow from '../components/survey_answer_page_components/ButtonRow.jsx';

const AnswerSurveyPage = () => {
  const { surveyId } = useParams();
  const { showNotification } = useNotification();
  const [neutral, setNeutral] = useState([]);
  const [good, setGood] = useState([]);
  const [bad, setBad] = useState([]);
  const [loading, setLoading] = useState(true);
  const [survey, setSurvey] = useState({});
  const [additionalInfo, setAdditionalInfo] = useState(false);
  const [expandedIds, setExpandedIds] = useState(new Set());
  const [reason, setReason] = useState("");
  const [existing, setExisting] = useState(false);
  const mountedRef =  useRef(false);

  useEffect(() => {
    mountedRef.current = true;
    (async () => {
      try {
        const data = await surveyService.getSurvey(surveyId);
        if (!mountedRef.current) return;

        const choices = data.choices || [];
        let neutralChoices = [...choices];
        let goodChoices = [];
        let badChoices = [];

        if (data.existing === "1") {
          setExisting(true);
          const goodIds = data.goodChoices || [];
          const badIds = data.badChoices || [];
          const goodIdSet = new Set((goodIds || []).map(String));
          const badIdSet = new Set((badIds || []).map(String));
          goodChoices = choices.filter((c) => goodIdSet.has(String(c.id)));
          badChoices = choices.filter((c) => badIdSet.has(String(c.id)));
          
          const used = new Set([...goodChoices, ...badChoices].map((c) => String(c.id)));
          neutralChoices = choices.filter((c) => !used.has(String(c.id)));
          
          setReason(data.reason || "");
        }
        setNeutral(neutralChoices);
        setGood(goodChoices);
        setBad(badChoices);
        setSurvey(data.survey || {});
        setAdditionalInfo(data.additional_info || false);
        
      } catch (err) {
        console.error(err);
      } finally {
        if (mountedRef.current) setLoading(false);
      }
      })();
    return () => { mountedRef.current = false; };
  }, [surveyId]);

  const handleDragEnd = (result) => {
    const { source, destination } = result;
      if (!destination) return;

    const sourceList = getList(source.droppableId);
    const destList = getList(destination.droppableId);
    const [moved] = sourceList.splice(source.index, 1);
    destList.splice(destination.index, 0, moved);

    updateList(source.droppableId, sourceList);
    updateList(destination.droppableId, destList);
  };

  const getList = (id) => {
    switch (id) {
      case "neutral": return neutral;
      case "good": return good;
      case "bad": return bad;
      default: return [];
    }
  };

  const updateList = (id, newList) => {
    switch (id) {
      case "neutral": setNeutral(newList); break;
      case "good": setGood(newList); break;
      case "bad": setBad(newList); break;
      default: break;
    }
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

  const handleSubmit = async () => {
    try {
      const result = await surveyService.submitSurveyAnswer({ surveyId: surveyId, good: good.map(c => c.id), bad: bad.map(c => c.id), neutral: neutral.map(c => c.id), reason, minChoices: survey.min_choices, deniedAllowedChoices: survey.denied_allowed_choices })
      if (result.status === "0") throw new Error(result.msg);
      showNotification(result.msg, "success");
      setExisting(true)
    } catch (error) {
      showNotification(error.message, "error");
      console.error("Error submitting survey", error);
    }
  };

  const handleDelete = async () => {
    try {
      const result = await surveyService.deleteSurveyAnswer(surveyId);
      if (result.status === "0") throw new Error(result.msg);
      showNotification(result.msg, "success");
      setExisting(false);
      setNeutral([...neutral, ...good, ...bad]);
      setGood([]);
      setBad([]);
      setReason("");
    } catch (error) {
      showNotification(error.message, "error");
      console.error("Error deleting survey", error);
    }
  };

  const readOnly = Boolean(survey.closed);

  if (loading) return <div className="text-center mt-5">Loading survey...</div>;
  
  return (
    <div className="answer-page">
      <div>
        <Header surveyName={survey.name} />
        {!readOnly && ( <SurveyInfo survey={survey} additionalInfo={additionalInfo} />)}
      </div>
      {readOnly ? (
        <ClosedSurveyView good={good} bad={bad} neutral={neutral} expandedIds={expandedIds} toggleExpand={toggleExpand} reason={reason} existing={existing} />
      ) : (
        <div className="answer-layout">
          <DragDropContext onDragEnd={handleDragEnd} context={ReactReduxContext}>
            <div className="left-column">
              <GroupList
              id="good"
                items={good}
                expandedIds={expandedIds}
                toggleExpand={toggleExpand}
                choices={neutral} 
              />
              { (survey.denied_allowed_choices ?? 0) !== 0 && (
                <>
                  <GroupList
                    id="bad"
                    items={bad}
                    expandedIds={expandedIds}
                    toggleExpand={toggleExpand}
                    choices={neutral}
                  />
                  <ReasonsBox reason={reason} setReason={setReason} />
                </>
              )}
              <ButtonRow handleSubmit={handleSubmit} handleDelete={handleDelete} existing={existing} />
            </div>
            <div className="right-column">
              <GroupList
                id="neutral"
                items={neutral}
                expandedIds={expandedIds}
                toggleExpand={toggleExpand}
                choices={neutral}
              />
            </div>
          </DragDropContext>
        </div>
      )}
  </div>
  );
};

export default AnswerSurveyPage;