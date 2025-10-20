import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import assignmentWhite from "/images/assignment_white_36dp.svg";
import emailWhite from "/images/email_white_36dp.svg";
import doneWhite from "/images/done_white_36dp.svg";
import questionAnswerWhite from "/images/question_answer_white_36dp.svg";
import personOffWhite from "/images/person_off_white_36dp.svg";

const SurveyAnswersPage = () => {
  const [answers, setAnswers] = useState([]);
  const [surveyData, setSurveyData] = useState({})
  const { id } = useParams();
  const { t } = useTranslation()

  useEffect(() => {
    const getSurveyAnswersData = async () => {
      try {
        const responseData = await surveyService.getSurveyAnswersData(id);
        setAnswers(responseData.surveyAnswers)
        setSurveyData(responseData)
      } catch (err) {
        console.error("Error loading survey data", err);
      }
    }
    getSurveyAnswersData()
  }, []);

  return (
    <div>
      <br />
      <h5>
        <img 
          src={assignmentWhite}
          alt=""
          width={34}
          height={30}
        />
        &nbsp;{surveyData.surveyName}
      </h5>
      <br />
      <i>{t("Vastauksia")}: {surveyData.surveyAnswersAmount}</i>
      <br />
      <i>{t("Jaettavia paikkoja")}: {surveyData.availableSpaces}</i>
      <br />
      <br />
      <a 
        href="/surveys"
        className="surveys_link"
        style={{ float: "right" }}
        >
          {t("Palaa kyselylistaan")}  
      </a>
      <br />
      <br />
      <button className="btn btn-outline-primary">
        {t("Jaa ryhmiin")}
      </button>
      <button className="btn btn-outline-warning" style={{ float: "right" }}>
        {t("Avaa kysely uudelleen")}
      </button>
      <br />
      <br />
      <p>
        <i style={{ whiteSpace: "pre-line" }}>
          {t(`Hae yksittäistä vastausta kirjoittamalla tähän kenttään
            vastaajan sähköposti tai osa siitä`)}
        </i>
        <br />
        <input 
          type="email"
          name="search_email"
          id="search_email"
        />
      </p>
      <table cellSpacing={10} className="table table-striped">
        <thead className="table-dark">
          <tr>
            <th>
              <img 
                src={emailWhite}
                alt=""
                width={24}
                height={24}
                className="d-inline-block align-text-top"
              />
              &nbsp;{t("Sähköposti")}
            </th>
            <th style={{minWidth: "12em"}}>
              <img 
                src={doneWhite}
                alt=""
                width={24}
                height={24}
                className="d-inline-block align-text-top"
              />
              &nbsp;{t("Valinnat")}
            </th>
            <th>
              <img 
                src={questionAnswerWhite}
                alt=""
                width={24}
                height={24}
                className="d-inline-block align-text-top"
              />
              &nbsp;{t("Perustelut")}
            </th>
            <th>
              <img 
                src={personOffWhite}
                alt=""
                width={24}
                height={24}
                className="d-inline-block align-text-top"
              />
              &nbsp;{t("Vastauksen poistaminen")}
            </th>
          </tr>
        </thead>
        <tbody>
          {answers.map(a => (
            <tr>
              <td>
                <p>
                  {a.email}
                </p>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  )
};

export default SurveyAnswersPage;