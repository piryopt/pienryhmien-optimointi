import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import feedbackService from "../../services/feedback"
import { useNotification } from "../../context/NotificationContext"

const AdminFeedbackList = () => {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const { showNotification } = useNotification()

  useEffect(() => {
    let mounted = true
    const load = async () => {
      setLoading(true)
      const res = await feedbackService.fetchOpenFeedbacks()
      if (!res.success) {
        showNotification(res.message || "Failed to load feedbacks", "error")
      } else if (mounted) {
        setItems(res.data)
      }
      setLoading(false)
    }
    load()
    return () => { mounted = false }
  }, [])

  return (
    <div>
      <h2>Avoimet palautteet</h2>
      {loading ? <p>Loading...</p> : (
        <table className="table table-striped">
          <thead className="table-dark">
            <tr>
              <th>Otsikko</th><th>Tyyppi</th><th>Sähköposti</th><th>Tarkastele</th>
            </tr>
          </thead>
          <tbody>
            {items.map(f => (
              <tr key={f[0] || f.id}>
                <td>{f[1] || f.title}</td>
                <td>{f[2] || f.type}</td>
                <td>{f[3] || f.email}</td>
                <td>
                  <Link to={`/admintools/feedback/${f[0] || f.id}`}>Lisää</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default AdminFeedbackList