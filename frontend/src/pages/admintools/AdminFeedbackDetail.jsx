import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import feedbackService from "../../services/feedback"
import { useNotification } from "../../context/NotificationContext"

const AdminFeedbackDetail = () => {
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
        showNotification(res.message || "Failed to load", "error")
      } else if (mounted) {
        setFeedback(res.data)
      }
      setLoading(false)
    }
    load()
    return () => { mounted = false }
  }, [id])

  const onClose = async () => {
    if (!window.confirm("Haluatko varmasti sulkea palautteen?")) return
    setClosing(true)
    const res = await feedbackService.closeFeedback(id)
    setClosing(false)
    if (!res.success) {
      showNotification(res.message || "Failed to close", "error")
      return
    }
    showNotification("Palaute suljettu", "success")
    navigate("/admintools/feedback")
  }

  if (loading) return <p>Loading...</p>
  if (!feedback) return <p>Ei palautetta</p>

  return (
    <div>
      <h2>{feedback[1] || feedback.title}</h2>
      <p><strong>Tyyppi:</strong> {feedback[2] || feedback.type}</p>
      <p><strong>Lähettäjä:</strong> {feedback[3] || feedback.email}</p>
      <div><p>{feedback[4] || feedback.content}</p></div>
      {!feedback[5] && (
        <button className="btn btn-warning" onClick={onClose} disabled={closing}>
          {closing ? "Suljetaan..." : "Sulje palaute"}
        </button>
      )}
    </div>
  )
}

export default AdminFeedbackDetail