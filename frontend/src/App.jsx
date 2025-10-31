import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthProvider";
import SurveyMultiphaseCreate from "./pages/SurveyMultiphaseCreate";
import SurveysPage from "./pages/SurveysPage";
import LoginPage from "./pages/LoginPage";
import Layout from "./components/Layout";
import FAQ from "./components/footer_components/FAQ";
import PrivacyPolicy from "./components/footer_components/PrivacyPolicy";
import SurveyAnswersPage from "./pages/SurveyAnswersPage";
import FrontPage from "./pages/FrontPage";
import SurveyResultsPage from "./pages/SurveyResultsPage";
import FeedbackPage from "./pages/FeedbackPage";
import AdminFeedbackList from "./pages/admintools/AdminFeedbackList"
import AdminClosedFeedbackList from "./pages/admintools/AdminClosedFeedbackList"
import AdminFeedbackDetail from "./pages/admintools/AdminFeedbackDetail"
import RequireAuth from "./components/RequireAuth";
import RequireAdmin from "./components/RequireAdmin"
import AnswerSurveyPage from "./pages/AnswerSurveyPage";

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route
              path="/multiphase/survey/create"
              element={
                <RequireAuth>
                  <SurveyMultiphaseCreate />
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
              path="/surveys/:surveyId"
              element={
                <RequireAuth>
                  <AnswerSurveyPage />
                </RequireAuth>
              }
            />
            <Route path="/auth/login" element={<LoginPage />} />

            <Route path="/faq" element={<FAQ />} />

            <Route path="/privacy-policy" element={<PrivacyPolicy />} />

            <Route
              path="/"
              element={
                <RequireAuth>
                  <FrontPage />
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
              path="/surveys/:id/results"
              element={
                <RequireAuth>
                  <SurveyResultsPage />
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
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
