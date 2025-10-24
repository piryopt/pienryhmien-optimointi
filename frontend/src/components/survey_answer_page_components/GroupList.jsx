import { Droppable, Draggable } from "@hello-pangea/dnd";

const GroupList = ({ id, items = [], expandedIds, toggleExpand, allInfo }) => {
  const borderColor = id === "good" ? "green" : id === "bad" ? "darkred" : "gray";

  return (
    <Droppable droppableId={id}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          style={{
            padding: 5,
            marginBottom: 25,
            width: 550,
            minHeight: 100,
            border: `2px solid ${borderColor}`,
            marginRight: 20,
            borderRadius: 6,
          }}
        >
          {items.map((item, index) => (
            <Draggable key={item.id} draggableId={item.id} index={index}>
              {(provided) => (
                <div
                  ref={provided.innerRef}
                  {...provided.draggableProps}
                  {...provided.dragHandleProps}
                  onClick={() => toggleExpand(item.id)}
                  role="button"
                  tabIndex={0}
                  style={{
                    borderRadius: "12px",
                    paddingLeft: "12px",
                    paddingBottom: "8px",
                    marginBottom: "6px",
                    border: "1px solid #5c5c5cff",
                    WebkitBoxShadow: "0px 2px 7px 0px rgba(0,0,0,0.75)",
                    MozBoxShadow: "0px 2px 1px 0px rgba(0,0,0,0.75)",
                    boxShadow: "0px 2px 7px 0px rgba(0,0,0,0.75)",
                    backgroundColor: "rgb(24, 26, 27)",
                    cursor: "pointer",
                    userSelect: "none",
                    ...provided.draggableProps.style
                  }}
                >
                  <h2 style={{ fontSize: "20px", margin: "7px 0 0 0" }}>{item.name}</h2>
                  <p style={{ fontSize: "15px", margin: "6px 0 0 0" }}>Ryhmän maksimikoko: {item.slots}</p>
                  {item.mandatory && <p style={{ fontSize: "15px", margin: "0" }}>Ryhmän minimikoko: {item.min_size}</p>}

                  {expandedIds.has(item.id.toString()) && (
                    <div style={{ marginTop: 8, paddingTop: 8, color: "#cfcfcf" }}>
                      {allInfo[item.id] && Array.isArray(allInfo[item.id].infos) && allInfo[item.id].infos.length > 0 ? (
                        allInfo[item.id].infos.map((infoObj, idx) => {
                          const entries = Object.entries(infoObj);
                          const [key, value] = entries.length ? entries[0] : ["", ""];
                          return (
                            <div key={idx} style={{ marginBottom: 6, fontSize: 14 }}>
                              <strong style={{ marginRight: 6 }}>{key}:</strong>
                              <span>{value}</span>
                            </div>
                          );
                        })
                      ) : (
                        <p style={{ margin: 0, fontSize: 14 }}>Lisätietoa ei saatavilla.</p>
                      )}
                    </div>
                  )}
                </div>
              )}
            </Draggable>
          ))}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );
};

export default GroupList;