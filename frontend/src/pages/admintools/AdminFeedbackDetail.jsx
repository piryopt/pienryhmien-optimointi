import { useEffect, useState } from "react";
import { Link, useParams, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import feedbackService from "../../services/feedback";
import { useNotification } from "../../context/NotificationContext";

const AdminFeedbackDetail = () => {
  const { t } = useTranslation("misc");
  const { id } = useParams();
  const navigate = useNavigate();
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(null);
  const [closing, setClosing] = useState(null);
  const { showNotification } = useNotification();

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      try {
        const res = await feedbackService.fetchFeedback(id);
        if (!res.success) {
          showNotification(res.message || t("Lataus epäonnistui"), "error");
          navigate("/");
          return;
        }
        if (mounted) setFeedback(res.data);
      } catch (err) {
        console.error("Failed to load feedback detail:", err);
        showNotification(t("Lataus epäonnistui"), "error");
      } finally {
        if (mounted) setLoading(false);
      }
    };
    load();
    return () => {
      mounted = false;
    };
  }, [id, showNotification, t]);

  const onClose = async () => {
    if (!window.confirm(t("Haluatko varmasti sulkea palautteen?"))) return;
    setClosing(true);
    const res = await feedbackService.closeFeedback(id);
    setClosing(false);
    if (!res.success) {
      showNotification(res.message || t("Sulkeminen epäonnistui"), "error");
      return;
    }
    showNotification(t("Palaute suljettu"), "success");
    navigate("/admintools/feedback");
  };

  if (loading) return <p>{t("Ladataan...")}</p>;
  if (!feedback) return <p>{t("Ei palautetta")}</p>;

  const backPath = feedback.solved
    ? "/admintools/feedback/closed"
    : "/admintools/feedback";

  return (
    <div>
      <br />
      <div style={{ marginBottom: 8 }}>
        <Link to={backPath}>
          <small>{t("Palaa listaan")}</small>
        </Link>
      </div>

      <h2>{feedback.title}</h2>
      <p>
        <strong>{t("Palautteen tyyppi")}</strong> {feedback.type}
      </p>
      <p>
        <strong>{t("Palautteen lähettäjä")}:</strong> {feedback.email || "-"}
      </p>
      <div>
        <p>{feedback.content}</p>
      </div>
      {!feedback.solved && (
        <button
          className="btn btn-warning"
          onClick={onClose}
          disabled={closing}
        >
          {closing ? t("Suljetaan...") : t("Sulje palaute")}
        </button>
      )}
    </div>
  );
};

export default AdminFeedbackDetail;
