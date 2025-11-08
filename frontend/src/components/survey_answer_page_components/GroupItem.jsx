import "../../static/css/answerPage.css";

const GroupItem = ({ item, choice, expanded, onToggle, index, id }) => {
  return (
    <div
      key={String(item.id)}
      onClick={() => onToggle(String(item.id))}
      role="button"
      tabIndex={0}
      className="group-item"
    >
      <h2 className="group-item-title">
        {id === "good" && <span className="rank-number">{index}. </span>}
        <span
          style={{ marginLeft: id === "good" ? "10px" : "0px", width: "100%" }}
          className="group-name"
        >
          {item.name}
        </span>
        {item.mandatory && <span className="group-mandatory">Pakollinen</span>}
      </h2>
      <p className="group-slots">Ryhmän maksimikoko: {item.slots}</p>
      {item.mandatory && (
        <p className="group-minsize">Ryhmän minimikoko: {item.min_size}</p>
      )}
      {expanded && (
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
  );
};

export default GroupItem;
