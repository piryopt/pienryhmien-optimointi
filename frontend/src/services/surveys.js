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

const getDeletedSurveys = async () => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/deleted`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getSurvey = async (surveyId) => {
  try {
    const response = await axios.get(`${baseUrl}/surveys/${surveyId}`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getFrontPageData = async () => {
  try {
    const response = await axios.get(`${baseUrl}/frontpage`, {
      withCredentials: true
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};

const trashSurvey = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.patch(
      `${baseUrl}/surveys/${surveyId}/trash`,
      null,
      {
        headers: {
          "Content-Type": "application/json",
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

const returnSurvey = async (surveyId) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.patch(
      `${baseUrl}/surveys/${surveyId}/return`,
      null,
      {
        headers: {
          "Content-Type": "application/json",
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
      `${baseUrl}/surveys/${surveyId}`,
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
    const response = await axios.delete(
      `${baseUrl}/surveys/${surveyId}/submission`,
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

const deleteSurveyAnswerByEmail = async (surveyId, studentEmail) => {
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

const getMultiStageSurveyAnswersData = async (surveyId) => {
  try {
    const response = await axios.get(
      `${baseUrl}/surveys/multistage/${surveyId}/answers`,
      {
        withCredentials: true
      }
    );
    return response.data;
  } catch (error) {
    throw error;
  }
};

const getStudentRankings = async (surveyId, studentEmail, stage) => {
  try {
    if (stage) {
      const response = await axios.get(
        `${baseUrl}/surveys/${surveyId}/${stage}/studentranking/${studentEmail}`,
        {
          withCredentials: true
        }
      );
      return response.data;
    }
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

const openSurvey = async (surveyId, newEndDate, newEndTime) => {
  try {
    const csrfToken = await csrfService.fetchCsrfToken();
    const response = await axios.post(
      `${baseUrl}/surveys/${surveyId}/open`,
      { newEndDate, newEndTime },
      {
        headers: {
          "Content-Type": "application/json",
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
      `${baseUrl}/surveys/multistage/${payload.surveyId}`,
      {
        stages: payload.stages,
        minChoices: payload.minChoices,
        deniedAllowedChoices: payload.deniedAllowedChoices
      },
      {
        headers: {
          "X-CSRFToken": csrfToken
        },
        withCredentials: true
      }
    );

    if (response.data.status === "1") {
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
      `${baseUrl}/surveys/multistage/${surveyId}`,
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
  getDeletedSurveys: getDeletedSurveys,
  getSurvey: getSurvey,
  getFrontPageData: getFrontPageData,
  submitSurveyAnswer: submitSurveyAnswer,
  deleteSurveyAnswer: deleteSurveyAnswer,
  deleteSurveyAnswerByEmail: deleteSurveyAnswerByEmail,
  trashSurvey: trashSurvey,
  returnSurvey: returnSurvey,
  deleteSurvey: deleteSurvey,
  getSurveyAnswersData: getSurveyAnswersData,
  getStudentRankings: getStudentRankings,
  openSurvey: openSurvey,
  closeSurvey: closeSurvey,
  getSurveyResultsData: getSurveyResultsData,
  saveResults: saveResults,
  submitMultiStageAnswers: submitMultiStageAnswers,
  getMultiStageSurvey: getMultiStageSurvey,
  getMultiStageSurveyAnswersData: getMultiStageSurveyAnswersData
};
