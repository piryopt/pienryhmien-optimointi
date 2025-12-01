import { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useNotification } from "../../context/NotificationContext";
import surveyService from "../../services/surveys";

const GroupSizesEditDialog = ({ surveyId, onClose, onSuccess }) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const [saving, setSaving] = useState(false);
  const [survey, setSurvey] = useState(null);
  const [choices, setChoices] = useState([]);
  const [surveyAnswersAmount, setSurveyAnswersAmount] = useState(0);
  const [editedChoices, setEditedChoices] = useState({});

  useEffect(() => {
    const loadGroupSizesData = async () => {
      try {
        const data = await surveyService.getGroupSizesData(surveyId);
        setSurvey(data.survey);
        setChoices(data.choices || []);
        setSurveyAnswersAmount(data.survey_answers_amount || 0);
        // Initialize edited choices with current values
        const initialEdited = {};
        (data.choices || []).forEach((choice) => {
          initialEdited[choice.id] = String(choice.max_spaces ?? "");
        });
        setEditedChoices(initialEdited);
      } catch (err) {
        console.error("Error loading group sizes data", err);
        onClose();
      }
    };

    loadGroupSizesData();
  }, [surveyId]);

  const handleSeatsChange = (choiceId, newValue) => {
    setEditedChoices((prev) => ({
      ...prev,
      [choiceId]: newValue
    }));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      const updatedChoices = choices.map((choice) => {
        const raw = editedChoices[choice.id];
        const seats = raw === undefined || raw === "" ? 0 : parseInt(raw, 10) || 0;
        return { id: choice.id, max_spaces: seats };
      });

      await surveyService.updateGroupSizes(surveyId, updatedChoices);
      showNotification(
        t("Ryhmäkoot päivitettiin onnistuneesti"),
        "success"
      );
      if (onSuccess) {
        onSuccess();
      }
      onClose();
    } catch (err) {
      showNotification(
        t("Ryhmäkokojen päivittäminen epäonnistui"),
        "error"
      );
      console.error("Error saving group sizes", err);
    } finally {
      setSaving(false);
    }
  };

  const getTotalEditedSpaces = useCallback(() => {
    return Object.values(editedChoices).reduce((sum, val) => {
      const n = val === undefined || val === "" ? 0 : parseInt(val, 10) || 0;
      return sum + n;
    }, 0);
  }, [editedChoices]);

  const validateInputs = useCallback(() => {
    const errors = [];

    choices.forEach((choice) => {
      const raw = editedChoices[choice.id];
      const seats = raw === undefined || raw === "" ? 0 : parseInt(raw, 10) || 0;

      if (seats <= 0) {
        errors.push(
          t('Ryhmä "{{name}}" täytyy sisältää vähintään 1 paikan', { name: choice.name })
        );
      }
    });

    const total = getTotalEditedSpaces();
    if (total < surveyAnswersAmount) {
      errors.push(
        t('Jaettavia paikkoja on {{total}}, mutta vastauksia on {{answers}}. Lisää paikkoja.', {
          total: total,
          answers: surveyAnswersAmount
        })
      );
    }

    return errors;
  }, [choices, editedChoices, getTotalEditedSpaces, surveyAnswersAmount, t]);

  const handleSaveWithValidation = useCallback(async () => {
    const errors = validateInputs();
    if (errors.length > 0) {
      errors.forEach((error) => {
        showNotification(error, "error");
      });
      return;
    }

    await handleSave();
  }, [validateInputs, handleSave, showNotification]);

  return (
    <div className="group-sizes-dialog-content">
      <h3>{survey?.surveyname}</h3>
      <p>
        <i>{t("Vastauksia")}: {surveyAnswersAmount}</i>
        <br />
        <i>{t("Jaettavia paikkoja")}: {getTotalEditedSpaces()}</i>
      </p>
      <p>
        <b>
          {t("Kyselyssä on enemmän vastaajia kuin jaettavia paikkoja. Muokkaa ryhmäkokoja ennen ryhmäjakoa.")}
        </b>
      </p>

      <div className="group-sizes-table-wrapper">
        <table className="table table-dark table-striped table-hover group-sizes-table">
          <thead>
            <tr>
              <th>{t("Nimi")}</th>
              <th>{t("Enimmäispaikat")}</th>
            </tr>
          </thead>
          <tbody>
            {choices.map((choice) => (
              <tr key={choice.id}>
                <td>{choice.name}</td>
                <td>
                  <input
                    type="number"
                    min="0"
                    value={editedChoices[choice.id] !== undefined ? editedChoices[choice.id] : String(choice.max_spaces)}
                    onChange={(e) => handleSeatsChange(choice.id, e.target.value)}
                    className="form-control form-control-sm"
                    disabled={saving}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div>
        <button
          className="btn btn-primary"
          onClick={handleSaveWithValidation}
          disabled={saving}
        >
          {t("Tallenna muutokset")}
        </button>
        <button
          className="btn btn-secondary"
          onClick={onClose}
          disabled={saving}
          style={{ marginLeft: "0.5em" }}
        >
          {t("Peruuta")}
        </button>
      </div>
    </div>
  );
};

export default GroupSizesEditDialog;
