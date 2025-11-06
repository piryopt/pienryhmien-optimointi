import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import { useTranslation } from "react-i18next";
import "../../static/css/dark.css";

const StageDropdown = ({ stages, currStage, setCurrStage }) => {
  const { t } = useTranslation();

  return (
    <div style={{ display: "inline-block" }}>
      <DropdownButton
        id="stage-dropdown"
        title={t("Valitse vaihe")}
        variant="dark"
        style={{ paddingTop: "1em", paddingBottom: "1em" }}
      >
        {stages.map((s, i) => (
          <Dropdown.Item
            key={i}
            active={currStage === s}
            onClick={() => setCurrStage(s)}
            style={{ color: "white" }}
          >
            {s}
          </Dropdown.Item>
        ))}
      </DropdownButton>
    </div>
  );
};

export default StageDropdown;
