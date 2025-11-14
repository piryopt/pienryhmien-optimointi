import ReactDOM from "react-dom/client";
import { imagesBaseUrl } from "./utils/constants";
import { BrowserRouter } from "react-router-dom";
import App from "./App";

import "./i18n";

document.documentElement.style.setProperty(
  "--delete-row-icon",
  `url("${imagesBaseUrl}/delete_white_36dp.svg")`
);
document.documentElement.style.setProperty(
  "--delete-col-icon",
  `url("${imagesBaseUrl}/delete_white_36dp.svg")`
);

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
