
const ReasonsBox = ({ reason, setReason }) => {
  return (
    <div style={{ width: "100%", marginTop: 8 }}>

      <textarea
        id="bad-reason"
        value={reason}
        onChange={(e) => setReason(e.target.value)}
        maxLength={300}
        placeholder="Kirjoita tähän perustelut hylkäyksille..."
        style={{
          width: "550px",
          minHeight: 80,
          resize: "vertical",
          padding: 8,
          borderRadius: 6,
          border: "1px solid rgba(255,255,255,0.08)",
          background: "rgba(54, 54, 54, 0.4)",
          color: "#fff",
        }}
      />
      <div style={{ marginTop: 6, fontSize: 12, color: "#bbb" }}>
        {reason.length}/300 merkkiä
      </div>
    </div>
  )
};

export default ReasonsBox;