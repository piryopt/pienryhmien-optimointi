import axios from 'axios';
const baseUrl = "http://localhost:5001"


const getActiveSurveys = () => (
  axios.get(`${baseUrl}/surveys/active`)
);

const getClosedSurveys = () => (
  axios.get(`${baseUrl}/surveys/closed`)
);

export default {
  getActiveSurveys: getActiveSurveys,
  getClosedSurveys: getClosedSurveys
}