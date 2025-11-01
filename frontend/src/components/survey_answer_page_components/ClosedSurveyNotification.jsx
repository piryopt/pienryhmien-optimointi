import '../../static/css/answerPage.css';
import closedIcon from '/images/warning_amber_white_36dp.svg';

const ClosedSurveyNotification = ({ existing }) => {
    console.log("ClosedSurveyNotification existing:", existing);
  return (
    <div className="closed-survey-notifier">
        <div className="closed-survey-icon">
            <img src={closedIcon} alt="" width="100%" height="100%" className="d-inline-block align-text-middle" />
        </div>
        <div className="closed-survey-content">
            <h2>Kysely on suljettu</h2>
            <p> Tämä kysely on suljettu eikä siihen voi enää vastata.
                {existing ? (
                    <> Vastauksesi kyselyyn on talletettu ja näet tekemäsi valinnat alta.</>
                ) : (
                    <> Et ole vastannut tähän kyselyyn.</>
                )}
            </p>
        </div>
    </div>
  );
};

export default ClosedSurveyNotification;