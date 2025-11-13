import { useTranslation } from "react-i18next";
import Table from "../Table";
import SurveyResultsTableRow from "./SurveyResultsTableRow";
import { imagesBaseUrl } from "../../utils/constants";

const SurveyResultsTable = ({ results, surveyId }) => {
  const { t } = useTranslation();

  const columns = [
    { title: t("Nimi"), icon: `${imagesBaseUrl}/person_off_white_36dp.svg` },
    { title: t("Sähköposti"), icon: `${imagesBaseUrl}/email_white_36dp.svg` },
    { title: t("Ryhmä"), icon: `${imagesBaseUrl}/groups_white_36dp.svg` },
    {
      title: t("Monesko valinta"),
      icon: `${imagesBaseUrl}/format_list_numbered_white_36dp.svg`
    },
    {
      title: t("Valinnat"),
      icon: `${imagesBaseUrl}/done_white_36dp.svg`,
      style: { minWidth: "12em" }
    }
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
