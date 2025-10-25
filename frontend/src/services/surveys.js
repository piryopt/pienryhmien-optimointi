import axios from 'axios';
import { baseUrl } from '../utils/constants';
import csrfService from './csrf';

const getActiveSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/active`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error
  }
};

const getClosedSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/closed`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error
  }
};

const getSurvey = async (surveyId) => {
  try {
    const response = await axios.get(`${baseUrl}/api/surveys/${surveyId}`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}

const deleteSurvey = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.delete(`${baseUrl}/surveys/${surveyId}`, {
      headers: {
        "X-CSRFToken": csrfToken
      },
      withCredentials: true
    })
    return response.data;
  } catch (error) {
    throw error;
  }
};

const submitSurveyAnswer = async ({surveyId, good, bad, neutral, reason, minChoices, deniedAllowedChoices }) =>  {
    const maxBadChoices = deniedAllowedChoices;
    const minC = minChoices;
    const neutralIds = neutral;
    const goodIds = good;
    const badIds = (maxBadChoices > 0) ? bad : [];
    const reasons = (maxBadChoices > 0) ? reason : "";

    const payload = {
        neutralIDs: neutralIds,
        goodIDs: goodIds,
        badIDs: badIds,
        allIDs: neutralIds.concat(goodIds, badIds),
        minChoices: minC,
        maxBadChoices: maxBadChoices,
        reasons: reasons
    };

    try {
      const csrfToken = await csrfService.fetchCsrfToken();
      const response = await axios.post(
        `${baseUrl}/api/surveys/${surveyId}`,
        payload,
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          }
        }
      );
      return response.data;
    } catch (error) {
      throw error;
    }
};

export default {
  getActiveSurveys: getActiveSurveys,
  getClosedSurveys: getClosedSurveys,
  getSurvey: getSurvey,
  deleteSurvey: deleteSurvey,
  submitSurveyAnswer: submitSurveyAnswer,
}