import { useTranslation } from "react-i18next"
import { useNotification } from "../context/NotificationContext"

const FeedbackPage = () => {
  const { t } = useTranslation()
  const { showNotification } = useNotification()

  const add_feedback = () => {
    <div>
      {showNotification("Palaute lähetetty")}
    </div>
  }

	return (
    <div>
      <br />
      <h2>{t("Palaute")}</h2>
      <div className="form-group">
        <label>{t("Otsikko")}</label>
        <input type="text" className="form-control" name="title" id="title" />
      </div><br />
      <div className="form-group">
        <label>{t("Palautteen tyyppi")}</label>
        <select className="form-select">
          <option value="palaute">{t("Palaute")}</option>
          <option value="bugi">{t("Bugi")}</option>
          <option value="muu">{t("Muu")}</option>
        </select>
      </div><br />
      <div className="form-group">
        <label>{t("Sisältö")}</label>
        <textarea className="form-control" rows="5" name="content" id="content" />
      </div> <br />
      <button type="submit" className="btn btn-primary" onClick={add_feedback}>{t("Anna palaute")}</button>
    </div>
	)
}

export default FeedbackPage