import { useTranslation } from "react-i18next";

const SurveyResultsTable = ({ results }) => {
  const { t } = useTranslation();

  return (
    <table 
      style={{ cellspacing: 10 }}
      className="table table-striped"
      >
        <thead className="table-dark">
          <tr>
            <th>{t("Nimi")}</th>
            <th>{t("Sähköposti")}</th>
            <th>{t("Ryhmä")}</th>
            <th>{t("Monesko valinta")}</th>
            <th>{t("Valinnat")}</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, i) => (
            /* for some reason,
              result = [[userId, username], email, [surveyChoiceId, name]] */
            <tr key={i}>
              <td>
                <p>
                  {result[0][1]}
                </p>
              </td>
              <td>
                <p>
                  {result[1]}
                </p>
              </td>
              <td>
                <p>
                  {result[2][1]}
                </p>
              </td>
              <td>
                <p>
                  {result[3]}
                </p>
              </td>
              <td>
                Näytä
              </td>
            </tr>
          ))}
        </tbody>
    </table>
  )
}

export default SurveyResultsTable;