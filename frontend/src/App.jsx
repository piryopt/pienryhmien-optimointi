import { Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthProvider";
import SurveyMultistageCreate from "./pages/SurveyMultistageCreate";
import SurveysPage from "./pages/SurveysPage";
import LoginPage from "./pages/LoginPage";
import Layout from "./components/Layout";
import FAQ from "./components/footer_components/FAQ";
import PrivacyPolicy from "./components/footer_components/PrivacyPolicy";
import SurveyAnswersPage from "./pages/SurveyAnswersPage";
import FrontPage from "./pages/FrontPage";
import SurveyResultsPage from "./pages/SurveyResultsPage";
import AdminAnalytics from "./pages/admintools/AdminAnalytics";
import AdminSurveyList from "./pages/admintools/AdminSurveyList";
import FeedbackPage from "./pages/FeedbackPage";
import AdminFeedbackList from "./pages/admintools/AdminFeedbackList";
import AdminClosedFeedbackList from "./pages/admintools/AdminClosedFeedbackList";
import AdminFeedbackDetail from "./pages/admintools/AdminFeedbackDetail";
import RequireAuth from "./components/RequireAuth";
import RequireAdmin from "./components/RequireAdmin";
import AnswerSurveyPage from "./pages/AnswerSurveyPage";
import CreateSurveyPage from "./pages/CreateSurveyPage";
import CSVInstructionsPage from "./components/create_survey_page_components/CSVInstructionsPage";
import MultiStageAnswerPage from "./pages/MultiStageAnswerPage";
import SurveyMultistageAnswersPage from "./pages/SurveyMultistageAnswersPage";
import MultistageResultsPage from "./pages/MultistageResultsPage";
import TrashPage from "./pages/TrashPage";
import EditSurveyPage from "./pages/EditSurveypage";

const App = () => {
  return (
    <AuthProvider>
      <Layout>
        <Routes>
          <Route
            path="/"
            element={
              <RequireAuth>
                <FrontPage />
              </RequireAuth>
            }
          />
          <Route
            path="/surveys"
            element={
              <RequireAuth>
                <SurveysPage />
              </RequireAuth>
            }
          />
          <Route
            path="/multistage/survey/create"
            element={
              <RequireAuth>
                <SurveyMultistageCreate />
              </RequireAuth>
            }
          />
          <Route
            path="/surveys/create"
            element={
              <RequireAuth>
                <CreateSurveyPage />
              </RequireAuth>
            }
          />
          <Route
            path="/surveys/:surveyId"
            element={
              <RequireAuth>
                <AnswerSurveyPage />
              </RequireAuth>
            }
          />
          <Route
            path="/surveys/multistage/:surveyId"
            element={
              <RequireAuth>
                <MultiStageAnswerPage />
              </RequireAuth>
            }
          />
          <Route path="/auth/login" element={<LoginPage />} />

          <Route path="/faq" element={<FAQ />} />

          <Route path="/privacy-policy" element={<PrivacyPolicy />} />

          <Route
            path="/csv-instructions"
            element={
              <RequireAuth>
                <CSVInstructionsPage />
              </RequireAuth>
            }
          />

          <Route
            path="/surveys/:id/answers"
            element={
              <RequireAuth>
                <SurveyAnswersPage />
              </RequireAuth>
            }
          />
          <Route
            path="/surveys/multistage/:surveyId/answers"
            element={
              <RequireAuth>
                <SurveyMultistageAnswersPage />
              </RequireAuth>
            }
          />
          <Route
            path="/surveys/:id/results"
            element={
              <RequireAuth>
                <SurveyResultsPage />
              </RequireAuth>
            }
          />
          <Route
            path="/surveys/multistage/:id/results"
            element={
              <RequireAuth>
                <MultistageResultsPage />
              </RequireAuth>
            }
          />
          <Route
            path="/trash"
            element={
              <RequireAuth>
                <TrashPage />
              </RequireAuth>
            }
          />
          <Route
            path="/feedback"
            element={
              <RequireAuth>
                <FeedbackPage />
              </RequireAuth>
            }
          />
          <Route
            path="/admintools/feedback"
            element={
              <RequireAuth>
                <RequireAdmin>
                  <AdminFeedbackList />
                </RequireAdmin>
              </RequireAuth>
            }
          />
          <Route
            path="/admintools/feedback/closed"
            element={
              <RequireAuth>
                <RequireAdmin>
                  <AdminClosedFeedbackList />
                </RequireAdmin>
              </RequireAuth>
            }
          />
          <Route
            path="/admintools/feedback/:id"
            element={
              <RequireAuth>
                <RequireAdmin>
                  <AdminFeedbackDetail />
                </RequireAdmin>
              </RequireAuth>
            }
          />
          <Route
            path="surveys/:id/edit" 
            element={
              <RequireAuth>
                <EditSurveyPage />
              </RequireAuth>
            }
          />
          <Route
            path="/admintools/analytics"
            element={
              <RequireAuth>
                <RequireAdmin>
                  <AdminAnalytics />
                </RequireAdmin>
              </RequireAuth>
            }
          />
          <Route
            path="/admintools/surveys"
            element={
              <RequireAuth>
                <RequireAdmin>
                  <AdminSurveyList />
                </RequireAdmin>
              </RequireAuth>
            }
          />
        </Routes>
      </Layout>
    </AuthProvider>
  );
};

export default App;
