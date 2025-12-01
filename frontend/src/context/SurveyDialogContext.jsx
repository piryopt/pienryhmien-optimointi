import { createContext, useContext, useState } from "react";
import { Modal, Button } from "react-bootstrap";
import { useTranslation } from "react-i18next";

const SurveyDialogContext = createContext();
export const useSurveyDialog = () => useContext(SurveyDialogContext);

export const SurveyDialogProvider = ({ children }) => {
  const { t } = useTranslation();

  const [dialogState, setDialogState] = useState({
    open: false,
    title: "",
    description: "",
    confirmData: null,
    onConfirmCallback: null,
    content: null
  });

  const openDialog = (
    title,
    description,
    confirmData,
    onConfirm,
    content = null
  ) => {
    setDialogState({
      open: true,
      title,
      description,
      confirmData,
      onConfirmCallback: () => onConfirm,
      content
    });
  };

  const closeDialog = () =>
    setDialogState({
      open: false,
      title: "",
      description: "",
      confirmData: null,
      onConfirmCallback: null
    });

  const onConfirm = () => {
    if (dialogState.onConfirmCallback) {
      if (dialogState.confirmData) {
        dialogState.onConfirmCallback()(dialogState.confirmData);
      } else {
        dialogState.onConfirmCallback()();
      }
    }
    closeDialog();
  };

  return (
    <SurveyDialogContext.Provider value={{ openDialog, closeDialog }}>
      {children}

      <Modal
        show={dialogState.open}
        onHide={closeDialog}
        centered
        contentClassName="bg-dark text-light"
      >
        <Modal.Header closeButton closeVariant="white">
          <Modal.Title>{dialogState.title}</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          {dialogState.content ? (
            <>
              {dialogState.content}
              <p className="mb-3">{dialogState.description}</p>
            </>
          ) : (
            <p className="mb-3">{dialogState.description}</p>
          )}
        </Modal.Body>

        {/* Hide default footer when passing hideModalFooter prop*/}
        {!(
          dialogState.content &&
          dialogState.content.props &&
          dialogState.content.props.hideModalFooter
        ) && (
          <Modal.Footer>
            <Button variant="secondary" onClick={closeDialog}>
              {t("Peruuta")}
            </Button>
            <Button variant="danger" onClick={onConfirm}>
              {t("Kyllä")}
            </Button>
          </Modal.Footer>
        )}
      </Modal>
    </SurveyDialogContext.Provider>
  );
};
