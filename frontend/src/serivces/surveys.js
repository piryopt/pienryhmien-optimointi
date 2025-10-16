import axios from 'axios';
const baseUrl = "http://localhost:5001"

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};

const getActiveSurveys = () => (
  axios.get(`${baseUrl}/surveys/active`)
);

const getClosedSurveys = () => (
  axios.get(`${baseUrl}/surveys/closed`)
);

const deleteSurvey = (surveyId) => (
  axios.delete(`${baseUrl}/surveys/${surveyId}`, {
    headers: {
      'X-CSRFToken': getCookie('csrf_token')
    }
  })
);

export default {
  getActiveSurveys: getActiveSurveys,
  getClosedSurveys: getClosedSurveys,
  deleteSurvey: deleteSurvey
}