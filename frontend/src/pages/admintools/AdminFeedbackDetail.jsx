import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { useTranslation } from "react-i18next"
import feedbackService from "../../services/feedback"
import { useNotification } from "../../context/NotificationContext"

const AdminFeedbackDetail = () => {
  const { t } = useTranslation()
  const { id } = useParams()
  const navigate = useNavigate()
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(null)
  const [closing, setClosing] = useState(null)
  const { showNotification } = useNotification()

  useEffect(() => {
    let mounted = true
    const load = async () => {
      setLoading(true)
      const res = await feedbackService.fetchFeedback(id)
      if (!res.success) {
        showNotification(res.message || t("Lataus epäonnistui"), "error")
      } else if (mounted) {
        setFeedback(res.data)
      }
      setLoading(false)
    }
    load()
    return () => { mounted = false }
  }, [id, showNotification, t])

  const onClose = async () => {
    if (!window.confirm(t("Haluatko varmasti sulkea palautteen?"))) return
    setClosing(true)
    const res = await feedbackService.closeFeedback(id)
    setClosing(false)
    if (!res.success) {
      showNotification(res.message || t("Sulkeminen epäonnistui"), "error")
      return
    }
    showNotification(t("Palaute suljettu"), "success")
    navigate("/admintools/feedback")
  }

  if (loading) return <p>{t("Ladataan...")}</p>
  if (!feedback) return <p>{t("Ei palautetta")}</p>

  return (
    <div>
      <h2>{feedback[1] || feedback.title}</h2>
      <p><strong>{t("Palautteen tyyppi")}</strong> {feedback.type}</p>
      <p><strong>{t("Palautteen lähettäjä")}:</strong> {feedback.email || "-"}</p>
      <div><p>{feedback.content}</p></div>
      {!feedback.solved && (
        <button className="btn btn-warning" onClick={onClose} disabled={closing}>
          {closing ? t("Suljetaan...") : t("Sulje palaute")}
        </button>
      )}
    </div>
  )
}

export default AdminFeedbackDetail
