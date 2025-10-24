import { useTranslation } from "react-i18next";

const UserRankings = ({ rankings, rejections }) => {
  const { t } = useTranslation();

  return (
    <div>
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
    </div>
  );
};

export default UserRankings;
