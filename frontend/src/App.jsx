import { BrowserRouter, Routes, Route } from "react-router-dom";
import SurveyMultiphaseCreate from "./components/SurveyMultiphaseCreate";
import SurveysPage from "./components/SurveysPage";
import LoginPage from "./components/LoginPage";
import Layout from "./components/Layout";

const App = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route
            path="/multiphase/survey/create"
            element={<SurveyMultiphaseCreate />}
          />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
