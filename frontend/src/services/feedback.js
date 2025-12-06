import axios from "axios";
import { baseUrl } from "../utils/constants";
import csrfService from "./csrf";

const validate = ({ title, content }) => {
  // Validation method for when creating new feedback.
  const t = (title || "").trim();
  const c = (content || "").trim();

  if (t.length < 3) {
    return {
      ok: false,
      key: "title_too_short",
      message: "Otsikko on liian lyhyt! Merkkimäärän täytyy olla vähintään 3."
    };
  }
  if (t.length > 50) {
    return {
      ok: false,
      key: "title_too_long",
      message: "Otsikko on liian pitkä! Merkkimäärä saa olla enintään 50."
    };
  }
  if (c.length < 5) {
    return {
      ok: false,
      key: "content_too_short",
      message: "Sisältö on liian lyhyt! Merkkimäärän täytyy olla vähintään 5."
    };
  }
  if (c.length > 1500) {
    return {
      ok: false,
      key: "content_too_long",
      message: "Sisältö on liian pitkä! Merkkimäärä saa olla enintään 1500."
    };
  }

  return { ok: true };
};

const createFeedback = async ({ title, type = "palaute", content }) => {
  // Sends a POST request with valid feedback
  const v = validate({ title, content });
  if (!v.ok) return { success: false, ...v };

  try {
    const csrfToken = await csrfService.fetchCsrfToken();
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
    );

    const data = response?.data || {};

    if (data.status === "1" || data.success === true) {
      return {
        success: true,
        id: data.id || null,
        key: data.key || "feedback_sent",
        message: data.msg || data.message || "Palaute lähetetty"
      };
    }
    return {
      success: false,
      key: data.key || "server_failed",
      message: data.msg || data.message || "Palautteen lähetys epäonnistui"
    };
  } catch (err) {
    return {
      success: false,
      key: "network_error",
      message:
        err?.response?.data?.message ||
        err?.response?.data?.msg ||
        err?.message ||
        "Yhteys palvelimeen epäonnistui"
    };
  }
};

const fetchOpenFeedbacks = async () => {
  /* Method for fetching all unresolved / open feedback.
  Only admins permitted! */
  try {
    const response = await axios.get(`${baseUrl}/admintools/feedback`, {
      withCredentials: true
    });
    const data = response?.data;
    return { success: true, data: data.data || data || [] };
  } catch (err) {
    return {
      success: false,
      message: err?.response?.data?.message || err?.message || "Network error"
    };
  }
};

const fetchClosedFeedbacks = async () => {
  /* Method for fetching all resolved / closed feedback.
  Only admins permitted! */
  try {
    const response = await axios.get(`${baseUrl}/admintools/feedback/closed`, {
      withCredentials: true
    });
    const data = response?.data || {};
    return { success: true, data: data.data || data || [] };
  } catch (err) {
    return {
      success: false,
      message: err?.response?.data?.message || err?.message || "Network error"
    };
  }
};

const fetchFeedback = async (id) => {
  /* Fetch further details about a specific piece of feedback.
  Only admins permitted! */
  try {
    const response = await axios.get(`${baseUrl}/admintools/feedback/${id}`, {
      withCredentials: true
    });
    const data = response?.data || {};
    if (!data.success)
      return { success: false, message: data.error || "Failed" };
    return { success: true, data: data.data };
  } catch (err) {
    return {
      success: false,
      message: err?.response?.data?.message || err?.message || "Network error"
    };
  }
};

const closeFeedback = async (id) => {
  /* Sends a POST request to close a given feedback. 
  Only admins permitted! */
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(
      `${baseUrl}/admintools/feedback/${id}/close`,
      {},
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        }
      }
    );
    const data = response?.data || {};
    return { success: data?.success === true, data };
  } catch (err) {
    return {
      success: false,
      message: err?.response?.data?.message || err?.message || "Network error"
    };
  }
};

export default {
  createFeedback,
  fetchOpenFeedbacks,
  fetchClosedFeedbacks,
  fetchFeedback,
  closeFeedback
};
