import { useTranslation } from "react-i18next";
import Table from "../Table";
import SurveyResultsTableRow from "./SurveyResultsTableRow";
import personWhite from "/images/person_off_white_36dp.svg";
import emailWhite from "/images/email_white_36dp.svg";
import groupsWhite from "/images/groups_white_36dp.svg";
import formatListNumberedWhite from "/images/format_list_numbered_white_36dp.svg";
import doneWhite from "/images/done_white_36dp.svg";

const SurveyResultsTable = ({ results, surveyId }) => {
  const { t } = useTranslation();

  const columns = [
    { title: t("Nimi"), icon: personWhite },
    { title: t("Sähköposti"), icon: emailWhite },
    { title: t("Ryhmä"), icon: groupsWhite },
    { title: t("Monesko valinta"), icon: formatListNumberedWhite },
    { title: t("Valinnat"), icon: doneWhite, style: { minWidth: "12em" } }
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
