import axios from "axios";
import { baseUrl } from "../utils/constants";
import csrfService from "./csrf";

const getActiveSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/api/surveys/active`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getClosedSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/api/surveys/closed`, {
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
};

const getFrontPageData = async () => {
  try {
    const response = await axios.get(`${baseUrl}/api/frontpage`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
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
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

const submitSurveyAnswer = async ({
  surveyId,
  good,
  bad,
  neutral,
  reason,
  minChoices,
  deniedAllowedChoices
}) => {
  const maxBadChoices = deniedAllowedChoices;
  const minC = minChoices;
  const neutralIds = neutral;
  const goodIds = good;
  const badIds = maxBadChoices > 0 ? bad : [];
  const reasons = maxBadChoices > 0 ? reason : "";

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

const deleteSurveyAnswer = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.delete(`${baseUrl}/api/surveys/${surveyId}`, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken
      },
      withCredentials: true
    });
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
    throw error;
  }
};

const saveResults = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(
      `${baseUrl}/surveys/${surveyId}/results`,
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

const submitMultiStageAnswers = async (payload) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(
      `${baseUrl}/api/surveys/multistage/${payload.surveyId}`,
      {
        stages: payload.stages,
        reason: payload.reason
      },
      {
        headers: {
          "X-CSRFToken": csrfToken
        },
        withCredentials: true
      }
    );

    if (response.data.success) {
      return { status: "1", msg: response.data.message || "success" };
    } else {
      return {
        status: "0",
        msg: response.data.message || "Error saving answers"
      };
    }
  } catch (error) {
    throw error;
  }
};

const getMultiStageSurvey = async (surveyId) => {
  try {
    const response = await axios.get(
      `${baseUrl}/api/surveys/multistage/${surveyId}`,
      {
        withCredentials: true
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
  getFrontPageData: getFrontPageData,
  deleteSurvey: deleteSurvey,
  submitSurveyAnswer: submitSurveyAnswer,
  deleteSurveyAnswer: deleteSurveyAnswer,
  deleteSurvey: deleteSurvey,
  getSurveyAnswersData: getSurveyAnswersData,
  getStudentRankings: getStudentRankings,
  openSurvey: openSurvey,
  closeSurvey: closeSurvey,
  getSurveyResultsData: getSurveyResultsData,
  saveResults: saveResults,
  submitMultiStageAnswers: submitMultiStageAnswers,
  getMultiStageSurvey: getMultiStageSurvey
};
