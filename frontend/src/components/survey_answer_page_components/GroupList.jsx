import { Droppable, Draggable } from "@hello-pangea/dnd";
import "../../static/css/answerPage.css";
import GroupItem from "./GroupItem";

const GroupList = ({
  id,
  items = [],
  expandedIds,
  toggleExpand,
  choices = [],
  readOnly = false,
  multiphase = false,
  searchTerm = ""
}) => {
  const borderColor = multiphase
    ? id.endsWith("good")
      ? "green"
      : id.endsWith("bad")
        ? "darkred"
        : "gray"
    : id === "good"
      ? "green"
      : id === "bad"
        ? "darkred"
        : "gray";
  const choiceMap = new Map(choices.map((c) => [String(c.id), c]));
  const normalizedSearch = (searchTerm || "").toString().trim().toLowerCase();

  if (readOnly) {
    const filteredItems = (items || []).filter((it) => {
      const name = it && it.name ? String(it.name).trim() : "";
      return name !== "Tyhjä";
    });

    return (
      <div className="group-container" style={{ marginBottom: 7 }}>
        {filteredItems.map((item, index) => (
          <GroupItem
            key={String(item.id)}
            item={item}
            choice={
              choiceMap.get(String(item.id)) || (item.infos ? item : null)
            }
            expanded={expandedIds.has(String(item.id))}
            onToggle={toggleExpand}
            index={index + 1}
            id={id}
          />
        ))}
      </div>
    );
  }

  const renderedItems = normalizedSearch
    ? (items || []).filter((it) => {
        if (!it) return false;
        const name = it.name ? String(it.name).toLowerCase() : "";
        if (name.includes(normalizedSearch)) return true;

        const choice = choiceMap.get(String(it.id)) || (it.infos ? it : null);
        if (choice && Array.isArray(choice.infos)) {
          for (const infoObj of choice.infos) {
            for (const val of Object.values(infoObj || {})) {
              if (
                val !== null &&
                val !== undefined &&
                String(val).toLowerCase().includes(normalizedSearch)
              ) {
                return true;
              }
            }
          }
        }
        return false;
      })
    : items || [];

  return (
    <Droppable droppableId={id}>
      {(provided) => (
        <div
          ref={provided.innerRef}
          {...provided.droppableProps}
          className="group-container"
          style={{ border: `2px solid ${borderColor}` }}
        >
          {renderedItems.map((item, index) => {
            const choice =
              choiceMap.get(String(item.id)) || (item.infos ? item : null);

            return (
              <Draggable
                key={String(item.id)}
                draggableId={String(item.id)}
                index={index}
              >
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    onClick={() => toggleExpand(String(item.id))}
                    role="button"
                    tabIndex={0}
                    className="group-item"
                    style={provided.draggableProps.style}
                  >
                    <h2 className="group-item-title">
                      {id.endsWith("good") && (
                        <span className="rank-number">{index + 1}. </span>
                      )}
                      <span
                        style={{
                          marginLeft: id.endsWith("good") ? "10px" : "0px"
                        }}
                        className="group-name"
                      >
                        {item.name}
                      </span>
                      {item.mandatory && (
                        <span className="group-mandatory">Pakollinen</span>
                      )}
                    </h2>
                    <p className="group-slots">
                      Ryhmän maksimikoko: {item.slots}
                    </p>
                    {item.mandatory && (
                      <p className="group-minsize">
                        Ryhmän minimikoko: {item.min_size}
                      </p>
                    )}

                    {expandedIds.has(String(item.id)) && (
                      <div className="group-expanded">
                        {choice &&
                        Array.isArray(choice.infos) &&
                        choice.infos.length > 0 ? (
                          (() => {
                            const visible = choice.infos
                              .map((infoObj) => {
                                const entries = Object.entries(infoObj);
                                const [key, value] = entries.length
                                  ? entries[0]
                                  : ["", ""];
                                return {
                                  key: key ? key.toString().trim() : "",
                                  value
                                };
                              })
                              .filter(
                                ({ key }) =>
                                  key !== "" &&
                                  !key.endsWith("*") &&
                                  !["hidden", "piilotettu"].includes(
                                    key.toLowerCase()
                                  )
                              );

                            if (visible.length === 0) {
                              return (
                                <p className="no-info">
                                  Lisätietoa ei saatavilla.
                                </p>
                              );
                            }

                            return visible.map((entry, idx) => (
                              <div key={idx} className="info-entry">
                                <strong className="info-key">
                                  {entry.key}:
                                </strong>
                                <span className="info-value">
                                  {entry.value}
                                </span>
                              </div>
                            ));
                          })()
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
