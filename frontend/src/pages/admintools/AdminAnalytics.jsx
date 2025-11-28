import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import adminService from "../../services/admin";
import { useNotification } from "../../context/NotificationContext";
import { Link, useNavigate } from "react-router-dom";

const AdminAnalytics = () => {
  const { t } = useTranslation();
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const { showNotification } = useNotification();
  const { navigate } = useNavigate();

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      const res = await adminService.fetchAnalytics();
      if (!res.success) {
        showNotification(
          res.message || t("Tilastojen lataus epäonnistui"),
          "error"
        );
        navigate("/");
      } else if (mounted) {
        const payload = res.data;
        let named = null;
        if (Array.isArray(payload)) {
          named = {
            total_surveys: payload[0] ?? 0,
            active_surveys: payload[1] ?? 0,
            total_students: payload[2] ?? 0,
            total_responses: payload[3] ?? 0,
            total_teachers: payload[4] ?? 0
          };
        } else if (payload && typeof payload === "object") {
          if (
            payload.total_surveys !== undefined ||
            payload.active_surveys !== undefined
          ) {
            named = {
              total_surveys: payload.total_surveys ?? 0,
              active_surveys: payload.active_surveys ?? 0,
              total_students: payload.total_students ?? 0,
              total_responses: payload.total_responses ?? 0,
              total_teachers: payload.total_teachers ?? 0
            };
          } else {
            named = {
              total_surveys:
                payload.created_by_distributor ?? payload.total_surveys ?? 0,
              active_surveys: payload.active_surveys ?? 0,
              total_students:
                payload.registered_students ?? payload.total_students ?? 0,
              total_responses:
                payload.responses_created ?? payload.total_responses ?? 0,
              total_teachers:
                payload.registered_teachers ?? payload.total_teachers ?? 0
            };
          }
        } else {
          named = {
            total_surveys: 0,
            active_surveys: 0,
            total_students: 0,
            total_responses: 0,
            total_teachers: 0
          };
        }
        setMetrics(named);
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
      <h2>{t("Tilastot")}</h2>
      <div style={{ marginBottom: 8 }}>
        <Link to="/admintools/feedback">
          <small>{t("Tarkastele palautteita")}</small>
        </Link>
        <br />
        <Link to="/admintools/surveys">
          <small>{t("Tarkastele kyselyitä")}</small>
        </Link>
      </div>

      {loading ? (
        <p>{t("Ladataan...")}</p>
      ) : (
        <>
          {!metrics ? (
            <p>{t("Ei tietoja")}</p>
          ) : (
            <table className="table table-striped">
              <thead className="table-dark">
                <tr>
                  <th>{t("Jakajassa luodut kyselyt")}</th>
                  <th>{t("Kaikki käynnissä olevat kyselyt")}</th>
                  <th>{t("Rekisteröityneet opettajat")}</th>
                  <th>{t("Rekisteröityneet opiskelijat")}</th>
                  <th>{t("Vastauksia luotu")}</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{metrics.total_surveys}</td>
                  <td>{metrics.active_surveys}</td>
                  <td>{metrics.total_teachers}</td>
                  <td>{metrics.total_students}</td>
                  <td>{metrics.total_responses}</td>
                </tr>
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  );
};

export default AdminAnalytics;
