import { BrowserRouter, Routes, Route } from "react-router-dom";;
import { AuthProvider } from "./context/AuthProvider";
import SurveyMultiphaseCreate from "./components/SurveyMultiphaseCreate";
import SurveysPage from "./components/SurveysPage";
import LoginPage from "./components/LoginPage";
import Layout from "./components/Layout";
import FAQ from "./components/footer_components/FAQ";
import PrivacyPolicy from "./components/footer_components/PrivacyPolicy";
import FrontPage from "./components/FrontPage";
import RequireAuth from "./components/RequireAuth";

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
          </Routes>
        </Layout>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
