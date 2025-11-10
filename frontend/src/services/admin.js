import axios from "axios"
import { baseUrl } from "../utils/constants"

const fetchAnalytics = async () => {
  try {
    const response = await axios.get(`${baseUrl}/api/admintools/analytics`, {
      withCredentials: true
    })
    const data = response?.data || {}
    return { success: true, data: data.data || data || [] }
  } catch (err) {
    return {
      success: false,
      message:
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        err?.message ||
        "Network error"
    }
  }
}

const fetchAdminSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/api/admintools/surveys`, {
      withCredentials: true
    })
    const data = response?.data || {}
    return { success: true, data: data.data || data || [] }
  } catch (err) {
    return {
      success: false,
      message:
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        err?.message ||
        "Network error"
    }
  }
}

export default {
  fetchAnalytics,
  fetchAdminSurveys
}
