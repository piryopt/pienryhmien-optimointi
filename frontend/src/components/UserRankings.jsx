import { useTranslation } from "react-i18next";

const UserRankings = ({ rankings, rejections, notAvailable = false }) => {
  const { t } = useTranslation();

  const notAvailableStyle = {
    color: "#ff5c5c",
    fontWeight: 500,
    fontSize: "0.9rem",
    padding: "0.4em 0.6em",
    borderRadius: "4px",
    display: "inline-block"
  };

  return (
    <div style={{ margin: notAvailable ? "1em 0" : 0 }}>
      {notAvailable ? (
        <span style={notAvailableStyle}>{t("Ei paikalla")}</span>
      ) : (
        <>
          <br />
          <b>{t("Valinnat")}</b>
          <ol>
            {rankings.map((r, i) => (
              <li key={i}>{r.name}</li>
            ))}
          </ol>
          {rejections.length > 0 && (
            <>
              <b>{t("Kielletyt")}</b>
              <ul>
                {rejections.map((r, i) => (
                  <li key={i}>{r.name}</li>
                ))}
              </ul>
            </>
          )}
        </>
      )}
    </div>
  );
};

export default UserRankings;
