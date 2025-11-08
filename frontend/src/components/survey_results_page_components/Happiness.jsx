import { useTranslation } from "react-i18next";

const Happiness = ({ happinessData, average }) => {
  const { t } = useTranslation();
  return (
    <>
      <b>
        {t("Ryhmävalintojen keskiarvo")}: {average}
      </b>
      {happinessData
        .map((d) => typeof d[0] === "string")
        .some((isString) => isString) && (
        <p>
          {t(
            "Huom! Se, että osa opiskelijoista on sijoitettu hylättyihin tai ei-järjestettyihin valintoihin ei vaikuta keskiarvoon."
          )}
        </p>
      )}
      <div>
        {happinessData.map((h, i) => (
          <div key={i}>
            <label
              style={{
                color:
                  h[0] === "Hylättyyn"
                    ? "red"
                    : h[0] === "Ei järjestettyyn"
                      ? "yellow"
                      : ""
              }}
            >
              {typeof h[0] === "number" ? h[0] : t(h[0])}
              {t(h[1])}
              {h[2]}
            </label>
          </div>
        ))}
      </div>
    </>
  );
};

export default Happiness;
