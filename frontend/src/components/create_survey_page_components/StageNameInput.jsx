import { useTranslation } from "react-i18next";
import "../../static/css/createSurveyPage.css";

const StageNameInput = ({ value = "", onChange = () => {}, id, placeholder, style }) => {
  const { t } = useTranslation();

  return (
    <input
      type="text"
      className="form-control"
      id={id || "stagename"}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder || t("Vaiheen nimi")}
    />
  );
};

export default StageNameInput;
