import axios from "axios"
import { baseUrl } from "../utils/constants"
import csrfService from "./csrf"

const validate = ({ title, content }) => {
  const t = (title || "").trim()
  const c = (content || "").trim()

  if (t.length < 3) {
    return { ok: false, key: "title_too_short", message: "Otsikko on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 3." }
  }
  if (t.length > 50) {
    return { ok: false, key: "title_too_long", message: "Otsikko on liian pitkä! Merkkimäärän täytyy olla pienempi kuin 50." }
  }
  if (c.length < 5) {
    return { ok: false, key: "content_too_short", message: "Sisältö on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 5." }
  }
  if (c.length > 1500) {
    return { ok: false, key: "content_too_long", message: "Sisältö on liian pitkä! Merkkimäärän täytyy olla pienempi kuin 1500." }
  }

  return { ok: true }
}

const createFeedback = async ({ title, type = "palaute", content }) => {
  const v = validate({ title, content })
  if (!v.ok) return { success: false, ...v }

  try {
    const csrfToken = await csrfService.fetchCsrfToken()
    const response = await axios.post(
      `${baseUrl}/feedback`,
      { title, type, content },
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }
    )
    const data = response?.data || {}

    if (data.status === "1" || data.success === true) {
      return { success: true, key: "feedback_sent", message: data.message || "Palaute lähetetty" }
    }
    return { success: false, key: "server_failed", message: data.message || "Palautteen lähetys epäonnistui" }
  } catch (err) {
    return {
      success: false,
      key: "network_error",
      message: err?.response?.data?.message || err?.message || "Yhteys palvelimeen epäonnistui" }
  }
}

export default { createFeedback }