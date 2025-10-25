import { Droppable, Draggable } from "@hello-pangea/dnd";
import '../../static/css/answerPage.css';

const GroupList = ({ id, items = [], expandedIds, toggleExpand, choices = [] }) => {
  const borderColor = id === "good" ? "green" : id === "bad" ? "darkred" : "gray";

  const choiceMap = new Map(choices.map((c) => [String(c.id), c]));

  return (
    <Droppable droppableId={id}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          className="group-container"
          style={{ border: `2px solid ${borderColor}` }} // keep dynamic border color inline
        >
          {items.map((item, index) => {
            const choice = choiceMap.get(String(item.id)) || (item.infos ? item : null);

            return (
              <Draggable key={String(item.id)} draggableId={String(item.id)} index={index}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    onClick={() => toggleExpand(String(item.id))}
                    role="button"
                    tabIndex={0}
                    className="group-item"
                    style={provided.draggableProps.style} // keep drag transform/position
                  >
                    <h2 className="group-item-title">
                      <span className="group-name">{item.name}</span>
                      {item.mandatory && (
                        <span className="group-mandatory">Pakollinen</span>
                      )}
                    </h2>
                    <p className="group-slots">Ryhmän maksimikoko: {item.slots}</p>
                    {item.mandatory && <p className="group-minsize">Ryhmän minimikoko: {item.min_size}</p>}

                    {expandedIds.has(String(item.id)) && (
                      <div className="group-expanded">
                        {choice && Array.isArray(choice.infos) && choice.infos.length > 0 ? (
                          choice.infos.map((infoObj, idx) => {
                            const entries = Object.entries(infoObj);
                            const [key, value] = entries.length ? entries[0] : ["", ""];
                            return (
                              <div key={idx} className="info-entry">
                                <strong className="info-key">{key}:</strong>
                                <span className="info-value">{value}</span>
                              </div>
                            );
                          })
                        ) : (
                          <p className="no-info">Lisätietoa ei saatavilla.</p>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </Draggable>
            );
          })}
          {provided.placeholder}
        </div>
      )}
    </Droppable>
  );
};


export default GroupList;