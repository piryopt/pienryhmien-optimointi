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
import RequireAuth from "./components/RequireAuth";
import AnswerSurveyPage from "./pages/AnswerSurveyPage";
import CreateSurvey from "./pages/CreateSurvey";

const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route
              path="/surveys/create"
              element={
                <RequireAuth>
                  <CreateSurvey />
                </RequireAuth>
              }
            />
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
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
