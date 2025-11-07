import { useTranslation } from "react-i18next";
import { Modal, Button } from "react-bootstrap";

const SurveysDialog = ({
  dialogOpen,
  setDialogOpen,
  onConfirm,
  confirmData,
  title,
  description
}) => {
  const { t } = useTranslation();

  return (
    <Modal
      show={dialogOpen}
      onHide={() => setDialogOpen(false)}
      centered
      contentClassName="bg-dark text-light"
    >
      <Modal.Header closeButton closeVariant="white">
        <Modal.Title>{title}</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <p className="mb-3">{description}</p>
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={() => setDialogOpen(false)}>
          {t("Peruuta")}
        </Button>
        <Button
          variant="danger"
          onClick={() => {
            setDialogOpen(false);
            onConfirm?.(confirmData);
          }}
        >
          {t("Kyllä")}
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default SurveysDialog;
