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

const deleteSurveyAnswer = async (surveyId, studentEmail) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(`${baseUrl}/surveys/${surveyId}/answers/delete`,
      {
        "student_email": studentEmail
      },
      {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken
      },
      withCredentials: true
    })
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getSurveyAnswersData = async (surveyId) => {
  try {
   const response = await axios.get(`${baseUrl}/surveys/${surveyId}/answers`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error
  }
}

const getStudentRankings = async (surveyId, studentEmail) => {
  try {
   const response = await axios.get(`${baseUrl}/surveys/${surveyId}/studentranking/${studentEmail}`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error
  }
}

export default {
  getActiveSurveys: getActiveSurveys,
  getClosedSurveys: getClosedSurveys,
  deleteSurvey: deleteSurvey,
  getSurveyAnswersData: getSurveyAnswersData,
  deleteSurveyAnswer: deleteSurveyAnswer,
  getStudentRankings: getStudentRankings,
}