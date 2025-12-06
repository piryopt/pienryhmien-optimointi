import axios from "axios";
import { baseUrl } from "../utils/constants";

const fetchAnalytics = async () => {
  /* Method for fetching analytics from the backend.
  Only admins permitted! */
  try {
    const response = await axios.get(`${baseUrl}/admintools/analytics`, {
      withCredentials: true
    });
    const data = response?.data || {};
    return { success: true, data: data.data || data || [] };
  } catch (err) {
    return {
      success: false,
      message:
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        err?.message ||
        "Network error"
    };
  }
};

const fetchAdminSurveys = async () => {
  /* Method for fetching a list of all active surveys.
  Only admins permitted! */
  try {
    const response = await axios.get(`${baseUrl}/admintools/surveys`, {
      withCredentials: true
    });
    const data = response?.data || {};
    return { success: true, data: data.data || data || [] };
  } catch (err) {
    return {
      success: false,
      message:
        err?.response?.data?.message ||
        err?.response?.data?.error ||
        err?.message ||
        "Network error"
    };
  }
};

export default {
  fetchAnalytics,
  fetchAdminSurveys
};
