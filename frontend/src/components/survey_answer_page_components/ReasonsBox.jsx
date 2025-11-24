import '../../static/css/answerPage.css';
import { useTranslation } from "react-i18next";

const ReasonsBox = ({ reason, setReason }) => {
  const { t } = useTranslation();
  return (
    <div style={{ width: "100%", marginTop: 8 }}>

      <textarea
        id="bad-reason"
        className="reason-textarea"
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        maxLength={300}
        placeholder={`${t('Kirjoita tähän perustelut hylkäyksille')}...`}
      />
      <div style={{ margin: 6, fontSize: 12, color: "#bbb" }}>
        {reason.length}/300 merkkiä
      </div>
    </div>
  )
};




export default ReasonsBox;