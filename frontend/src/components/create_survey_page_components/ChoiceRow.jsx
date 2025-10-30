import { useTranslation } from "react-i18next";

const ChoiceRow = ({ row, columns, updateCell, onDelete }) => {
  const { t } = useTranslation();

  const handleChange = (field) => (e) => {
    updateCell(
      row.id,
      field,
      e.target.type === "checkbox" ? e.target.checked : e.target.value
    );
  };

  return (
    <tr>
      <td style={{ textAlign: "center" }}>
        <input
          type="checkbox"
          checked={!!row.mandatory}
          onChange={handleChange("mandatory")}
        />
      </td>

      <td>
        <input
          type="text"
          value={row.name || ""}
          onChange={handleChange("name")}
        />
      </td>

      <td>
        <input
          type="text"
          value={row.max_spaces || ""}
          onChange={handleChange("max_spaces")}
        />
      </td>

      <td>
        <input
          type="text"
          value={row.min_size || ""}
          onChange={handleChange("min_size")}
        />
      </td>

      {columns.map((col) => (
        <td key={col.name}>
          <input
            type="text"
            value={row[col.name] || ""}
            onChange={handleChange(col.name)}
          />
        </td>
      ))}

      <td style={{ textAlign: "center" }}>
        <button type="button" onClick={onDelete}>
          {t("Poista")}
        </button>
      </td>
    </tr>
  );
};

export default ChoiceRow;
