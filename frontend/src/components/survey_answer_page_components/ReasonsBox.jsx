import '../../static/css/answerPage.css';

const ReasonsBox = ({ reason, setReason }) => {
  return (
    <div style={{ width: "100%", marginTop: 8 }}>

      <textarea
        id="bad-reason"
        className="reason-textarea"
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        maxLength={300}
        placeholder="Kirjoita tähän perustelut hylkäyksille..."
      />
      <div style={{ margin: 6, fontSize: 12, color: "#bbb" }}>
        {reason.length}/300 merkkiä
      </div>
    </div>
  )
};

export default ReasonsBox;