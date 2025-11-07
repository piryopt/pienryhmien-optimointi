import { useTranslation } from "react-i18next";
import { useNotification } from "../../context/NotificationContext";
import { useState } from "react";
import surveyService from "../../services/surveys";
import Table from "../Table";
import SurveyAnswersTableRow from "./SurveyAnswersTableRow";
import emailWhite from "/images/email_white_36dp.svg";
import doneWhite from "/images/done_white_36dp.svg";
import questionAnswerWhite from "/images/question_answer_white_36dp.svg";
import personOffWhite from "/images/person_off_white_36dp.svg";
import SurveysDialog from "../SurveysDialog";

const SurveyAnswersTable = (props) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [emailToDelete, setEmailToDelete] = useState("");

  const columns = [
    { title: t("Sähköposti"), icon: emailWhite },
    { title: t("Valinnat"), icon: doneWhite, style: { minWidth: "12em" } },
    { title: t("Perustelut"), icon: questionAnswerWhite },
    { title: t("Vastauksen poistaminen"), icon: personOffWhite }
  ];

  const handleAnswerDelete = (email) => {
    setEmailToDelete(email);
    setDialogOpen(true);
  };

  const deleteSurveyAnswer = (email) => {
    try {
      surveyService.deleteSurveyAnswerByEmail(props.surveyId, email);
      const updatedAnswers = props.answers.filter((a) => a.email !== email);
      const updatedFilteredAnswers = props.filteredAnswers.filter(
        (a) => a.email !== email
      );
      if (props.stage) {
        // make it work with current stage answers
        console.log(props);
      } else {
        props.setAnswers(updatedAnswers);
        props.setFilteredAnswers(updatedFilteredAnswers);
      }
      props.setSurveyAnswersAmount((prev) => prev - 1);
      showNotification(t("Vastaus poistettu"), "success");
    } catch (err) {
      showNotification(t("Vastauksen poistaminen epäonnistui"), "error");
      console.error("Error deleting answer:", err);
    }
  };

  return (
    <>
      <SurveysDialog
        dialogOpen={dialogOpen}
        setDialogOpen={setDialogOpen}
        title={t("Poista vastaus?")}
        description={t(
          `Haluatko varmasti poistaa käyttäjän ${emailToDelete} vastauksen?`
        )}
        onConfirm={deleteSurveyAnswer}
        confirmData={emailToDelete}
      />
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
    </>
  );
};

export default SurveyAnswersTable;
