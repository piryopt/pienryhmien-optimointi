import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { useTranslation } from "react-i18next"
import feedbackService from "../../services/feedback"
import { useNotification } from "../../context/NotificationContext"

const AdminClosedFeedbackList = () => {
  const { t } = useTranslation()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const { showNotification } = useNotification()

  useEffect(() => {
    let mounted = true
    const load = async () => {
      setLoading(true)
      const res = await feedbackService.fetchClosedFeedbacks()
      if (!res.success) {
        showNotification(res.message || t("Palautteiden lataus ei onnistunut"), "error")
      } else if (mounted) {
        setItems(res.data)
      }
      setLoading(false)
    }
    load()
    return () => { mounted = false }
  }, [showNotification, t])

  return (
    <div>
      <h2>{t("Suljetut palautteet")}</h2>
      {loading ? <p>{t("Ladataan...")}</p> : (
        <>
          {items.length === 0 ? <p>{t("Ei palautteita")}</p> : (
            <table className="table table-striped">
              <thead className="table-dark">
                <tr>
                  <th>{t("Otsikko")}</th><th>{t("Palautteen tyyppi")}</th><th>{t("Sähköposti")}</th><th>{t("Toiminnot")}</th>
                </tr>
              </thead>
              <tbody>
                {items.map(f => (
                  <tr key={f.id}>
                    <td>{f.title}</td>
                    <td>{f.type}</td>
                    <td>{f.email}</td>
                    <td>
                      <Link to ={`/admintools/feedback/${f.id}`}>{t("Tarkastele")}</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
    </div>
  )
}

export default AdminClosedFeedbackList