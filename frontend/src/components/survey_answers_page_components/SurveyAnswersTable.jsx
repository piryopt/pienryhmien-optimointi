import { useTranslation } from "react-i18next";
import { useNotification } from "../../context/NotificationContext";
import { useState } from "react";
import surveyService from "../../services/surveys";
import Table from "../Table";
import SurveyAnswersTableRow from "./SurveyAnswersTableRow";
import { useSurveyDialog } from "../../context/SurveyDialogContext";
import { imagesBaseUrl } from "../../utils/constants";

const SurveyAnswersTable = (props) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const { openDialog } = useSurveyDialog();

  const [emailToDelete, setEmailToDelete] = useState("");

  const columns = [
    { title: t("Sähköposti"), icon: `${imagesBaseUrl}/email_white_36dp.svg` },
    {
      title: t("Valinnat"),
      icon: `${imagesBaseUrl}/done_white_36dp.svg`,
      style: { minWidth: "12em" }
    },
    {
      title: t("Perustelut"),
      icon: `${imagesBaseUrl}/question_answer_white_36dp.svg`
    },
    {
      title: t("Vastauksen poistaminen"),
      icon: `${imagesBaseUrl}/person_off_white_36dp.svg`
    }
  ];

  const handleAnswerDelete = (email) => {
    setEmailToDelete(email);
    deleteSurveyAnswer(email);
  };

  const deleteSurveyAnswer = async (email) => {
    openDialog(
      t("Poista vastaus?"),
      t(`Haluatko varmasti poistaa käyttäjän ${emailToDelete} vastauksen?`),
      email,
      async () => {
        try {
          await surveyService.deleteSurveyAnswerByEmail(props.surveyId, email);
          const updatedAnswers = props.answers.filter((a) => a.email !== email);
          const updatedFilteredAnswers = props.filteredAnswers.filter(
            (a) => a.email !== email
          );
          props.setAnswers(updatedAnswers);
          props.setFilteredAnswers(updatedFilteredAnswers);
          props.setSurveyAnswersAmount((prev) => prev - 1);
          if (props.allAnswers) {
            const updatedAllAnswers = props.allAnswers.filter(
              (answer, i) => answer[props.stages[i]].email === email
            );
            props.setAllAnswers(updatedAllAnswers);
          }
          showNotification(t("Vastaus poistettu"), "success");
        } catch (err) {
          showNotification(t("Vastauksen poistaminen epäonnistui"), "error");
          console.error("Error deleting answer:", err);
        }
      }
    );
  };

  return (
    <Table
      columns={columns}
      data={props.filteredAnswers}
      renderRow={(answer, i) => (
        <SurveyAnswersTableRow
          key={i}
          answer={answer}
          surveyId={props.surveyId}
          handleAnswerDelete={handleAnswerDelete}
          stage={props.stage}
        />
      )}
    />
  );
};

export default SurveyAnswersTable;
