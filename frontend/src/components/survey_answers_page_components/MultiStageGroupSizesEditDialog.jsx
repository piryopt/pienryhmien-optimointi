import { useState, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useNotification } from "../../context/NotificationContext";
import surveyService from "../../services/surveys";

const MultiStageGroupSizesEditDialog = ({ surveyId, onClose, onSuccess }) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const [saving, setSaving] = useState(false);
  const [stages, setStages] = useState([]);
  const [answersByStage, setAnswersByStage] = useState({});
  const [availableSpaces, setAvailableSpaces] = useState({});
  const [editedChoices, setEditedChoices] = useState({});

  useEffect(() => {
    const load = async () => {
      try {
        const [stagesData, answersData] = await Promise.all([
          surveyService.getMultistageStages(surveyId),
          surveyService.getMultiStageSurveyAnswersData(surveyId)
        ]);
        const stagesList = stagesData || [];
        setStages(stagesList);

        const answers = answersData?.answers || [];
        // filter out answers where the respondent marked themselves not available
        const answersMap = {};
        answers.forEach((obj) => {
          const keys = Object.keys(obj);
          if (keys.length > 0) {
            const stageName = keys[0];
            answersMap[stageName] = (obj[stageName] || []).filter((a) => !a.notAvailable);
          }
        });
        setAnswersByStage(answersMap);
        setAvailableSpaces(answersData?.availableSpaces || {});

        const initial = {};
        stagesList.forEach((stage) => {
          (stage.choices || []).forEach((choice) => {
            initial[choice.id] = String(choice.slots ?? choice.max_spaces ?? "");
          });
        });
        setEditedChoices(initial);
      } catch (err) {
        console.error("Error loading multistage group sizes data", err);
        onClose();
      }
    };
    load();
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
      const updatedChoices = [];
      Object.keys(editedChoices).forEach((idStr) => {
        const id = parseInt(idStr, 10);
        const raw = editedChoices[idStr];
        const seats = raw === undefined || raw === "" ? 0 : parseInt(raw, 10) || 0;
        updatedChoices.push({ id, max_spaces: seats });
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
      console.error("Error saving multistage group sizes", err);
    } finally {
      setSaving(false);
    }
  };

  const getStageTotal = useCallback((stage) => {
    const total = (stage.choices || []).reduce((sum, c) => {
      const raw = editedChoices[c.id];
      const n = raw === undefined || raw === "" ? 0 : parseInt(raw, 10) || 0;
      return sum + n;
    }, 0);
    return total;
  }, [editedChoices]);

  const validateInputs = useCallback(() => {
    const errors = [];
    stages.forEach((stage) => {
      const answersCount = (answersByStage[stage.name] || []).length;
      const total = getStageTotal(stage);
      if (total < answersCount) {
        errors.push(
          t('Vaihe "{{name}}" sisältää {{total}} paikkaa, mutta vastauksia on {{answers}}. Lisää paikkoja vaiheeseen.', {
            name: stage.name,
            answers: answersCount,
            total: total
          })
        );
      }
      (stage.choices || []).forEach((choice) => {
        const raw = editedChoices[choice.id];
        const seats = raw === undefined || raw === "" ? 0 : parseInt(raw, 10) || 0;

        if (seats <= 0) {
          errors.push(
            t('Ryhmä "{{name}}" täytyy sisältää vähintään 1 paikan', { name: choice.name })
          );
        }
      });
    });
    return errors;
  }, [stages, editedChoices, answersByStage, getStageTotal, t]);

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

  const stagesNeedingEdit = stages.filter((stage) => {
    const answersCount = (answersByStage[stage.name] || []).length;
    const available = availableSpaces[stage.name] ?? 0;
    return answersCount > available;
  });

  return (
    <div className="group-sizes-dialog-content">
      <p>
        <b>
          {t("Kyselyn vaiheissa on enemmän vastaajia kuin jaettavia paikkoja. Muokkaa vaiheiden ryhmäkokoja ennen ryhmäjakoa.")}
        </b>
      </p>

      {stagesNeedingEdit.map((stage) => (
        <div key={stage.name} style={{ marginBottom: "1rem" }}>
          <h3>{stage.name}</h3>
          <p>
            <i>{t("Vastauksia")}: {(answersByStage[stage.name] || []).length}</i>
            <br />
            <i>{t("Jaettavia paikkoja")}: {getStageTotal(stage)}</i>
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
                {(stage.choices || []).map((choice) => (
                  <tr key={choice.id}>
                    <td>{choice.name}</td>
                    <td>
                      <input
                        type="number"
                        min="0"
                        value={editedChoices[choice.id] !== undefined ? editedChoices[choice.id] : String(choice.slots ?? choice.max_spaces)}
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
        </div>
      ))}
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

export default MultiStageGroupSizesEditDialog;
