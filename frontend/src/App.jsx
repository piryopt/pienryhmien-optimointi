import { BrowserRouter, Routes, Route } from "react-router-dom";
import FrontPage from "./components/FrontPage";
import SurveyMultiphaseCreate from "./components/SurveyMultiphaseCreate";
import SurveysPage from "./components/SurveysPage";
import LoginPage from "./components/LoginPage";
import Layout from "./components/Layout";
import FAQ from "./components/footer_components/FAQ";
import PrivacyPolicy from "./components/footer_components/PrivacyPolicy";
const App = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<FrontPage />} />
          <Route
            path="/multiphase/survey/create"
            element={<SurveyMultiphaseCreate />}
          />
          <Route path="/surveys" element={<SurveysPage />} />
          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/faq" element={<FAQ />} />
          <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
