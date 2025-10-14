import { BrowserRouter, Routes, Route } from "react-router-dom";
import SurveyMultiphaseCreate from "./components/SurveyMultiphaseCreate";
const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/multiphase/survey/create"
          element={<SurveyMultiphaseCreate />}
        />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
