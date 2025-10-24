import { useState, useEffect, useRef } from "react";
import { DragDropContext } from "@hello-pangea/dnd";
import { useParams } from "react-router-dom";
import surveyService from '../services/surveys';
import Button from 'react-bootstrap/Button';
import GroupList from '../components/survey_answer_page_components/GroupList.jsx';
import ReasonsBox from '../components/survey_answer_page_components/ReasonsBox.jsx';

const AnswerSurvey = () => {
  const { surveyId } = useParams();
  const [neutral, setNeutral] = useState([]);
  const [good, setGood] = useState([]);
  const [bad, setBad] = useState([]);
  const [loading, setLoading] = useState(true);
  const [survey, setSurvey] = useState({});
  const [additionalInfo, setAdditionalInfo] = useState(false);
  const [allInfo, setAllInfo] = useState({});
  const [expandedIds, setExpandedIds] = useState(new Set());
  const [reason, setReason] = useState("");

  const mountedRef =  useRef(false);

  useEffect(() => {
    mountedRef.current = true;
    (async () => {
      try {
        const data = await surveyService.getSurvey(surveyId);
        if (!mountedRef.current) return;
        setNeutral(data.choices || []);
        setSurvey(data.survey || {});
        setAdditionalInfo(data.additional_info || false);
        setAllInfo(data.all_info || {});
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

  if (loading) return <div className="text-center mt-5">Loading survey...</div>;

  return (
    <div style={{ padding: 20 }}>
      <h1 style={{ fontSize: "25px"}}>{survey.name}</h1>
      <p>Vastausaika päättyy {survey.deadline}</p>
      <p>
        <i>Raahaa oikean reunan listasta vähintään {survey.min_choices} vaihtoehtoa vihreään laatikkoon.</i>
      {additionalInfo ? (
         <i style={{ color: "#0bdb2ed6" }}> Klikkaa valintavaihtoehtoa nähdäksesi siitä lisätietoa.</i>
      ) : (
         <></>
      )}
      </p>
      <p>HUOM! Tärkeäksi merkityt ryhmät priorisoidaan jakamisprosessissa. Ne täytetään aina vähintään minimikokoon asti vastauksista riippumatta.</p>

      <div style={{ display: "flex", minHeight: "100vh", paddingTop: 20 }}>
        <DragDropContext onDragEnd={handleDragEnd}>
          <div style={{ display: "flex", flexDirection: "column", marginRight: 20, flexShrink: 0 }}>
            <GroupList id="good" items={good} expandedIds={expandedIds} toggleExpand={toggleExpand} allInfo={allInfo} />
            { (survey.denied_allowed_choices ?? 0) !== 0 && (
              <>
                <GroupList id="bad" items={bad} expandedIds={expandedIds} toggleExpand={toggleExpand} allInfo={allInfo} />
                <ReasonsBox reason={reason} setReason={setReason} />
              </>
            )}
          
            <div style={{ width: "100%", display: "flex", justifyContent: "flex-start", marginTop: 8 }}>
              <Button variant="success" style={{ width: "auto" }} onClick={() => console.log("Submit Rankings", { good, bad, neutral })}>
                Lähetä valinnat
              </Button>
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <GroupList id="neutral" items={neutral} expandedIds={expandedIds} toggleExpand={toggleExpand} allInfo={allInfo} />
          </div>
        </DragDropContext>
      </div>
    </div>
  );
};

export default AnswerSurvey;
