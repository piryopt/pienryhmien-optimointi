export const isoToDDMM = (iso) => {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d)) return "";
  return `${String(d.getDate()).padStart(2, "0")}.${String(d.getMonth() + 1).padStart(2, "0")}.${d.getFullYear()}`;
};

export const padTimeHHMM = (value) => {
  if (!value) return "00:00";
  const match = value.match(/^(\d{1,2}):?(\d{2})?$/);
  if (!match) return "00:00";
  return `${String(match[1]).padStart(2, "0")}:${match[2] || "00"}`;
};
