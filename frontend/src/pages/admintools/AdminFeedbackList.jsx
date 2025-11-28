import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import feedbackService from "../../services/feedback";
import { useNotification } from "../../context/NotificationContext";
import FeedbackTable from "../../components/feedback_components/FeedbackTable";

const AdminFeedbackList = () => {
  const { t } = useTranslation();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const { showNotification } = useNotification();
  const { navigate } = useNavigate();

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      const res = await feedbackService.fetchOpenFeedbacks();
      if (!res.success) {
        showNotification(
          res.message || t("Palautteiden lataus epäonnistui"),
          "error"
        );
        navigate("/");
      } else if (mounted) {
        setItems(res.data);
      }
      setLoading(false);
    };
    load();
    return () => {
      mounted = false;
    };
  }, [showNotification, t]);

  return (
    <div>
      <br />
      <h2>{t("Avoimet palautteet")}</h2>
      <div style={{ marginBottom: 8 }}>
        <Link to="/admintools/analytics">
          <small>{t("Tarkastele tilastoja")}</small>
        </Link>
        <br />
        <Link to="/admintools/surveys">
          <small>{t("Tarkastele kyselyitä")}</small>
        </Link>
      </div>
      <div style={{ marginBottom: 8 }} align="right">
        <Link to="/admintools/feedback/closed">
          <small>{t("Suljetut palautteet")}</small>
        </Link>
      </div>

      {loading ? (
        <p>{t("Ladataan…")}</p>
      ) : (
        <>
          {items.length === 0 ? (
            <p>{t("Ei palautteita")}</p>
          ) : (
            <FeedbackTable items={items} />
          )}
        </>
      )}
    </div>
  );
};

export default AdminFeedbackList;
