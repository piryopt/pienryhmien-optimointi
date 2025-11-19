import { useTranslation } from "react-i18next";
const ChoiceRowDisplay = ({
  row,
  columns = [],
  limitParticipationVisible = false
}) => {
  const { t } = useTranslation();

  return (
    <tr>
      <td style={{ textAlign: "center" }}>
        <input type="checkbox" checked={!!row.mandatory} readOnly disabled />
      </td>

      <td>
        <input
          type="text"
          className="form-control form-control-sm"
          value={row.name || ""}
          readOnly
        />
      </td>

      <td>
        <input
          type="number"
          min="0"
          className="form-control form-control-sm"
          value={row.max_spaces ?? row.slots ?? ""}
          readOnly
        />
      </td>

      <td>
        <input
          type="number"
          min="0"
          className="form-control form-control-sm"
          value={row.min_size ?? ""}
          readOnly
        />
      </td>

      {limitParticipationVisible && (
        <td>
          <input
            type="number"
            min="0"
            className="form-control form-control-sm"
            value={row.participation_limit ?? ""}
            readOnly
          />
        </td>
      )}

      {columns.map((col) => (
        <td key={col.name}>
          <input
            type="text"
            className="form-control form-control-sm"
            value={row[col.name] ?? ""}
            readOnly
          />
        </td>
      ))}

      <td className="action-cell" style={{ textAlign: "center" }}>
        {/* empty cell to preserve table layout */}
      </td>
    </tr>
  );
};

export default ChoiceRowDisplay;
