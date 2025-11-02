import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { useTranslation } from "react-i18next"
import feedbackService from "../../services/feedback"
import { useNotification } from "../../context/NotificationContext"
import FeedbackTable from "../../components/feedback_components/FeedbackTable"

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
        showNotification(res.message || t("Palautteiden lataus epäonnistui"), "error")
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
      <br />
      <h2>{t("Suljetut palautteet")}</h2>
      <div style={{ marginBottom: 8 }}>
        <Link to="/admintools/feedback">
          <small>{t("Avoimet palautteet")}</small>
        </Link>
      </div>

      {loading ? <p>{t("Ladataan...")}</p> : (
        <>
          {items.length === 0 ? <p>{t("Ei palautteita")}</p> : <FeedbackTable items={items} />}
        </>
      )}
    </div>
  )
}

export default AdminClosedFeedbackList
