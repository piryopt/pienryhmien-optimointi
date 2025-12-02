import { useTranslation } from "react-i18next";
import "../../static/css/createSurveyPage.css";

const StageNameInput = ({
  value = "",
  onChange = () => {},
  id,
  placeholder
}) => {
  const { t } = useTranslation("create");

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
