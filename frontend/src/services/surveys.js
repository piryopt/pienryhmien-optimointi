import axios from "axios";
import { baseUrl } from "../utils/constants";
import csrfService from "./csrf";

const getActiveSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/active`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getClosedSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/closed`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
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
    });
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

const deleteSurveyAnswer = async (surveyId, studentEmail) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(
      `${baseUrl}/surveys/${surveyId}/answers/delete`,
      {
        student_email: studentEmail
      },
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken
        },
        withCredentials: true
      }
    );
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
    throw error;
  }
};

const getStudentRankings = async (surveyId, studentEmail) => {
  try {
    const response = await axios.get(
      `${baseUrl}/surveys/${surveyId}/studentranking/${studentEmail}`,
      {
        withCredentials: true
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

const openSurvey = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(
      `${baseUrl}/surveys/${surveyId}/open`,
      null,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken
        },
        withCredentials: true
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

const closeSurvey = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(
      `${baseUrl}/surveys/${surveyId}/close`,
      null,
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken
        },
        withCredentials: true
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getSurveyResultsData = async (surveyId) => {
   try {
   const response = await axios.get(`${baseUrl}/surveys/${surveyId}/results`, {
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
  getSurvey: getSurvey,
  deleteSurvey: deleteSurvey,
  submitSurveyAnswer: submitSurveyAnswer,
  deleteSurvey: deleteSurvey,
  getSurveyAnswersData: getSurveyAnswersData,
  deleteSurveyAnswer: deleteSurveyAnswer,
  getStudentRankings: getStudentRankings,
  openSurvey: openSurvey,
  closeSurvey: closeSurvey,
  getSurveyResultsData: getSurveyResultsData,
}
