import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useNotification } from "../context/NotificationContext";
import feedbackService from "../services/feedback";

const FeedbackPage = () => {
  // Page for users to submit feedback using a simple form.
  const { t } = useTranslation();
  const { showNotification } = useNotification();

  const [title, setTitle] = useState("");
  const [type, setType] = useState("palaute");
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(false);

  const add_feedback = async () => {
    setLoading(true);
    try {
      const result = await feedbackService.createFeedback({
        title,
        type,
        content
      });

      if (!result.success) {
        const msg =
          (result.key ? t(result.key) : null) ||
          result.message ||
          t("Palautteen lähetys epäonnistui");
        showNotification(msg, "error");
        return;
      }

      const successMsg =
        (result.key ? t(result.key) : null) ||
        result.message ||
        t("Palaute lähetetty");
      showNotification(successMsg, "success");

      setTitle("");
      setType("palaute");
      setContent("");
    } catch (err) {
      showNotification(t("Yhteys palvelimeen epäonnistui"), "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <br />
      <h2>{t("Palaute")}</h2>
      <div className="form-group">
        <label>{t("Otsikko")}</label>
        <input
          type="text"
          className="form-control"
          name="title"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>
      <br />
      <div className="form-group">
        <label>{t("Palautteen tyyppi")}</label>
        <select
          className="form-select"
          value={type}
          onChange={(e) => setType(e.target.value)}
        >
          <option value="palaute">{t("Palaute")}</option>
          <option value="bugi">{t("Bugi")}</option>
          <option value="muu">{t("Muu")}</option>
        </select>
      </div>
      <br />
      <div className="form-group">
        <label>{t("Sisältö")}</label>
        <textarea
          className="form-control"
          rows="5"
          name="content"
          id="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
      </div>
      <br />
      <button
        type="submit"
        className="btn btn-primary"
        onClick={add_feedback}
        disabled={loading}
      >
        {loading ? t("Lähetetään...") : t("Anna palaute")}
      </button>
    </div>
  );
};

export default FeedbackPage;
