import Button from "react-bootstrap/Button";
import { useTranslation } from "react-i18next";

const ButtonRow = ({ handleSubmit, handleDelete, existing }) => {
  const { t } = useTranslation();

  return (
    <div className="submit-row">
      <Button
        variant="success"
        className="submit-btn"
        data-testid="submit-button"
        onClick={handleSubmit}
      >
        {t(`${existing ? "Päivitä" : "Lähetä"} valinnat`)}
      </Button>
      {existing && (
        <Button
          variant="danger"
          className="submit-btn"
          data-testid="delete-button"
          onClick={handleDelete}
          style={{ marginLeft: "15px" }}
        >
          {t("Poista valinnat")}
        </Button>
      )}
    </div>
  );
};

export default ButtonRow;
