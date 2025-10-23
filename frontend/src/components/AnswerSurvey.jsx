import React, { useState, useEffect } from "react";
import { DragDropContext, Droppable, Draggable } from "@hello-pangea/dnd";
import { useParams } from "react-router-dom";
import { baseUrl } from "../utils/constants";

const AnswerSurvey = () => {
  const { surveyId } = useParams();
  const [neutral, setNeutral] = useState([]);
  const [good, setGood] = useState([]);
  const [bad, setBad] = useState([]);
  const [loading, setLoading] = useState(true);
  const [survey, setSurvey] = useState({});
  const [additionalInfo, setAdditionalInfo] = useState(false);

  useEffect(() => {
    fetch(`${baseUrl}/api/surveys/${surveyId}`)
      .then((res) => res.json())
      .then((data) => {
        setNeutral(data.choices || []);
        setLoading(false);
        setSurvey(data.survey || {});
        setAdditionalInfo(data.additional_info || false);
      })
      .catch((err) => console.error(err));
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

  const renderList = (id, items) => {
    const borderColor = id === "good" ? "green" : id === "bad" ? "darkred" : "gray";

    return (
      <Droppable droppableId={id}>
        {(provided) => (
          <div
            ref={provided.innerRef}
            {...provided.droppableProps}
          style={{
            padding: 10,
            width: 500,
            minHeight: 200,
            border: `1px solid ${borderColor}`,
            marginRight: 20
          }}
        >
          {items.map((item, index) => (
            <Draggable key={item.id} draggableId={item.id} index={index}>
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.draggableProps}
                  {...provided.dragHandleProps}
                  style={{
                    borderRadius: "12px",
                    paddingLeft: "12px",
                    paddingBottom: "8px",
                    marginBottom: "8px",
                    border: "1px solid #ccc",
                    WebkitBoxShadow: "0px 2px 7px 0px rgba(0,0,0,0.75)",
                    MozBoxShadow: "0px 2px 1px 0px rgba(0,0,0,0.75)",
                    boxShadow: "0px 2px 7px 0px rgba(0,0,0,0.75)",
                    backgroundColor: "rgb(24, 26, 27)",
                    ...provided.draggableProps.style
                  }}
                >
                  <h2 style={{"font-size":"20px", "margin": "7px 0px 0px 0px"}}>{item.name}</h2>
                  <p style={{"font-size":"15px", "margin": "6px 0px 0px 0px"}}>Ryhmän maksimikoko: {item.slots}</p>
                  {item.mandatory && <p style={{"font-size":"15px", "margin": "0px 0px 0px 0px"}}>Ryhmän minimi koko: {item.min_size}</p>}
                </div>
              )}
            </Draggable>
          ))}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );}

  if (loading) return <div className="text-center mt-5">Loading survey...</div>;

  return (
    <div>
      <h1>{survey.name}</h1>
      <p>Vastausaika päättyy {survey.deadline}</p>
      <p>
        <i>Raahaa oikean reunan listasta vähintään {survey.min_choices} vaihtoehtoa vihreään laatikkoon.</i>
      {additionalInfo ? (
         <i style={{ color: "#0bdb2ed6" }}> Klikkaa valintavaihtoehtoa nähdäksesi siitä lisätietoa.</i>
      ) : (
         <></>
      )}
      </p>

      <div style={{ display: "flex", padding: 20, minHeight: "100vh" }}>
        <DragDropContext onDragEnd={handleDragEnd}>
          <div style={{ display: "flex", flexDirection: "column", marginRight: 20, flexShrink: 0 }}>
            {renderList("good", good)}
            {renderList("bad", bad)}
            <button onClick={() => console.log("Submit Rankings", { good, bad, neutral })} style={{ marginTop: 20, padding: 10 }}>
              Submit Rankings
            </button>
          </div>
          <div style={{ flex: 1 }}>
            {renderList("neutral", neutral)}
          </div>
        </DragDropContext>
      </div>
    </div>
  );
};

export default AnswerSurvey;
