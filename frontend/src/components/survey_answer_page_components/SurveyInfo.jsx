import { useTranslation } from "react-i18next";

const SurveyInfo = ({ survey, additionalInfo, choices, stageName = null }) => {
  const { t } = useTranslation();
  const min_choices = !stageName
    ? Number(survey.min_choices)
    : Number(survey.min_choices_per_stage[stageName]);
  const a_d_c = Number(survey.denied_allowed_choices);
  const total = choices.length;

  const isAll = total > 0 && min_choices === total;
  const denySome = a_d_c > 0;

  return (
    <>
      <p className="deadline">{t('Vastausaika päättyy')} {survey.deadline}</p>
      <p style={{ padding: "1.5em 0" }}>{survey.description}</p>

      <p className="instructions">
        <i>
          {isAll && !denySome && (
            <>
              {t('Raahaa kaikki vaihtoehdot')}{" "}
              <span className="highlight-green">{t('vihreään')}</span> {t('laatikkoon')}.
            </>
          )}

          {isAll && denySome && (
            <>
              {t('Raahaa kaikki vaihtoehdot')}{" "}
              <span className="highlight-green">{t('vihreään')}</span> {t('tai')}{" "}
              <span className="highlight-red">{t('punaiseen')}</span> {t('laatikkoon')}.
              <br />
              <span>
                {t('Voit kieltää')} {a_d_c} {t('vaihtoehtoa')}{" "}
                <span className="highlight-red">{t('punaiseen')}</span> {t('laatikkoon')}.
              </span>
            </>
          )}

          {!isAll && !denySome && (
            <>
              {t('Raahaa ainakin')} {min_choices} {t('vaihtoehtoa')}{" "}
              <span className="highlight-green">{t('vihreään')}</span> {t('laatikkoon')}.
            </>
          )}

          {!isAll && denySome && (
            <>
              {t('Raahaa ainakin')} {min_choices} {t('vaihtoehtoa')}{" "}
              <span className="highlight-green">{t('vihreään')}</span> {t('tai')}{" "}
              <span className="highlight-red">{t('punaiseen')}</span> {t('laatikkoon')}.
              <br />
              <span>
                {t('Voit kieltää')} {a_d_c} {t('vaihtoehtoa')}{" "}
                <span className="highlight-red">{t('punaiseen')}</span> {t('laatikkoon')}.
              </span>
            </>
          )}
        </i>

        {additionalInfo ? (
          <i> {t('Klikkaa valintavaihtoehtoa nähdäksesi siitä lisätietoa')}.</i>
        ) : null}
      </p>
    </>
  );
};

export default SurveyInfo;
