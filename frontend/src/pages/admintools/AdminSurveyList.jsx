import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { format, parseISO, isValid, parse } from "date-fns";
import adminService from "../../services/admin";
import { useNotification } from "../../context/NotificationContext";

const AdminSurveyList = () => {
  const { t } = useTranslation();
  const [surveys, setSurveys] = useState([]);
  const [loading, setLoading] = useState(true);
  const { showNotification } = useNotification();
  const { navigate } = useNavigate();

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      const res = await adminService.fetchAdminSurveys();
      if (!res.success) {
        showNotification(
          res.message || t("Kyselyjen lataus epäonnistui"),
          "error"
        );
        navigate("/");
      } else if (mounted) {
        setSurveys(res.data || []);
      }
      setLoading(false);
    };
    load();
    return () => {
      mounted = false;
    };
  }, [showNotification, t]);

  const formatEndDate = (raw) => {
    if (raw === null || raw == undefined || raw === "") return "-";

    // If already a Date object
    if (raw instanceof Date) {
      if (!isValid(raw)) return "-";
      return format(raw, "yyyy-MM-dd HH:mm:ss");
    }

    // If it's a number
    if (typeof raw === "number") {
      const dnum = new Date(raw);
      if (isValid(dnum)) return format(dnum, "yyyy-MM-dd HH:mm:ss");
      return "-";
    }

    // If string, try multiple parsers
    if (typeof raw === "string") {
      // 1) ISO
      let d = parseISO(raw);
      if (isValid(d)) return format(d, "yyyy-MM-dd HH:mm:ss");

      // 2) Common DB format "yyyy-MM-dd HH:mm:ss"
      try {
        d = parse(raw, "yyyy-MM-dd HH:mm:ss", new Date());
        if (isValid(d)) return format(d, "yyyy-MM-dd HH:mm:ss");
      } catch (e) {
        // Ignore and continue
      }

      // 3) Native Date parser (RFC1123)
      d = new Date(raw);
      if (isValid(d)) return format(d, "yyyy-MM-dd HH:mm:ss");

      // 4) Try swapping first space to 'T' to mimic ISO
      const maybeIso = raw.replace(" ", "T");
      d = parseISO(maybeIso);
      if (isValid(d)) return format(d, "yyyy-MM-dd HH:mm:ss");

      return "-";
    }
    return "-";
  };

  return (
    <div>
      <br />
      <h2>{t("Kyselyt")}</h2>
      <div style={{ marginBottom: 8 }}>
        <Link to="/admintools/feedback">
          <small>{t("Tarkastele palautteita")}</small>
        </Link>
        <br />
        <Link to="/admintools/analytics">
          <small>{t("Tarkastele tilastoja")}</small>
        </Link>
      </div>

      {loading ? (
        <p>{t("Ladataan...")}</p>
      ) : (
        <>
          {surveys.length === 0 ? (
            <p>{t("Ei kyselyitä")}</p>
          ) : (
            <table className="table table-striped">
              <thead className="table-dark">
                <tr>
                  <th>{t("ID")}</th>
                  <th>{t("Nimi")}</th>
                  <th>{t("Min valinnat")}</th>
                  <th>{t("Ryhmien määrä")}</th>
                  <th>{t("Kieltomäärä")}</th>
                  <th>{t("Päättyy")}</th>
                  <th>{t("Toiminnot")}</th>
                </tr>
              </thead>
              <tbody>
                {surveys.map((s, idx) => {
                  const id = s[0] ?? `row-${idx}`;
                  const name = s[1] ?? "-";
                  const minChoices = s[2] ?? "-";
                  const endRaw = s[3] ?? null;
                  const deniedAllowed = s[4] ?? "-";
                  const searchVisibility = s[5] ? t("Kyllä") : t("Ei");
                  const numGroups = s[6] ?? "-";
                  return (
                    <tr key={id}>
                      <td>{id}</td>
                      <td>{name}</td>
                      <td>{minChoices}</td>
                      <td>{numGroups}</td>
                      <td>{deniedAllowed}</td>
                      <td>{formatEndDate(endRaw)}</td>
                      <td>{searchVisibility}</td>
                      <td>
                        <Link to={`/surveys/${id}/answers`}>{t("Avaa")}</Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  );
};

export default AdminSurveyList;
