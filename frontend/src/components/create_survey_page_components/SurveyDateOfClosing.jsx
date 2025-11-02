import { useFormContext, Controller } from "react-hook-form";
import DatePicker from "react-datepicker";
import { format } from "date-fns";
import { useTranslation } from "react-i18next";
import "react-datepicker/dist/react-datepicker.css";

const hours = Array.from({ length: 24 }).map(
  (_, i) => String(i).padStart(2, "0") + ":00"
);

const SurveyDateOfClosing = () => {
  const { t } = useTranslation();
  const { control, register, formState } = useFormContext();
  const { errors } = formState;

  return (
    <section>
      <h2>{t("Vastausaika")}</h2>
      <p>
        {t(
          "Vastausaika määrittää aikavälin, jolloin kyselyyn on mahdollista vastata."
        )}
      </p>

      <label className="deadline">{t("Vastausaika päättyy")}:</label>

      <div className="datetime-controls">
        <div className="datetime-field datetime-date">
          <Controller
            name="enddate"
            control={control}
            render={({ field }) => (
              <DatePicker
                {...field}
                id="end-date"
                className={`datetime-input-field ${errors.enddate ? "is-invalid" : ""}`}
                selected={field.value || null}
                onChange={(date) => field.onChange(date)}
                dateFormat="dd.MM.yyyy"
                minDate={new Date()}
                placeholderText={t("pp.kk.vvvv")}
                autoComplete="off"
              />
            )}
          />
        </div>

        <div className="datetime-field datetime-time">
          <label htmlFor="endtime" className="time-label">
            {t("Kello")}:
          </label>
          <select
            id="endtime"
            {...register("endtime")}
            className={`datetime-input-field time-select ${errors.endtime ? "is-invalid" : ""}`}
            defaultValue={hours[0]}
          >
            {hours.map((h) => (
              <option key={h} value={h}>
                {h}
              </option>
            ))}
          </select>
        </div>
      </div>

      <ul className="validation-warnings-list">
        <li>
          <span
            className="input-validation-warning"
            id="enddate-validation-warning"
          >
            {errors.enddate?.message}
          </span>
        </li>
        <li>
          <span
            className="input-validation-warning"
            id="endtime-validation-warning"
          >
            {errors.endtime?.message}
          </span>
        </li>
      </ul>
    </section>
  );
};

export default SurveyDateOfClosing;
