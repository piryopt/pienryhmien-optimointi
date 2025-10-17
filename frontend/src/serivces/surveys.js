import axios from 'axios';
import { baseUrl } from '../utils/constants';
import csrfService from './csrfService';

const getActiveSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/active`)
    return response.data
  } catch (error) {
    throw error
  }
};

const getClosedSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/closed`)
    return response.data
  } catch (error) {
    throw error
  }
};

const deleteSurvey = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken()
    const response = await axios.delete(`${baseUrl}/surveys/${surveyId}`, {
      headers: {
        "X-CSRFToken": csrfToken
      },
         withCredentials: true
    })
    return response.data
  } catch (error) {
    throw error
  }
};

export default {
  getActiveSurveys: getActiveSurveys,
  getClosedSurveys: getClosedSurveys,
  deleteSurvey: deleteSurvey
}