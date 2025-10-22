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

  useEffect(() => {
    fetch(`${baseUrl}/api/surveys/${surveyId}`)
      .then((res) => res.json())
      .then((data) => {
        setNeutral(data.choices || []);
        setLoading(false);
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

  const renderList = (id, items) => (
    <Droppable droppableId={id}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          style={{
            padding: 10,
            width: 400,
            minHeight: 200,
            border: "1px solid gray",
            marginRight: 20
          }}
        >
          <h4>{id.toUpperCase()}</h4>
          {items.map((item, index) => (
            <Draggable key={item.id} draggableId={item.id} index={index}>
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.draggableProps}
                  {...provided.dragHandleProps}
                  style={{
                    padding: 8,
                    margin: "0 0 8px 0",
                    backgroundColor: "#eee",
                    borderRadius: 4,
                    ...provided.draggableProps.style
                  }}
                >
                  {item.name}
                </div>
              )}
            </Draggable>
          ))}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );

  if (loading) return <div className="text-center mt-5">Loading survey...</div>;

  return (
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
  );
};

export default AnswerSurvey;
