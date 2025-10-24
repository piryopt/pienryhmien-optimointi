import { useTranslation } from "react-i18next";
import Table from "../Table";
import SurveyResultsTableRow from "./SurveyResultsTableRow";

const SurveyResultsTable = ({ results, surveyId }) => {
  const { t } = useTranslation();

  const columns = [
    { title: t("Nimi"), logo: "" },
    { title: t("Sähköposti"), logo: "" },
    { title: t("Ryhmä"), logo: "" },
    { title: t("Monesko valinta"), logo: "" },
    { title: t("Valinnat"), logo: "", style: { minWidth: "12em" } }
  ];

  return (
    <Table
      columns={columns}
      data={results}
      renderRow={(result, i) => (
        <SurveyResultsTableRow key={i} result={result} surveyId={surveyId} />
      )}
    />
  );
};

export default SurveyResultsTable;
