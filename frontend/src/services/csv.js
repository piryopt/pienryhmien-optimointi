export async function parseCsvFile(file) {
  if (!file) return [];
  const text = await file.text();
  return parseCSV(text);
}

export function parseCSV(text) {
  const lines = text.replace(/\r\n/g, "\n").split("\n").filter((l) => l.trim() !== "");
  return lines.map((line) => {
    const row = [];
    let cur = "";
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (ch === '"') {
        if (inQuotes && line[i + 1] === '"') {
          cur += '"';
          i++;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (ch === "," && !inQuotes) {
        row.push(cur);
        cur = "";
      } else {
        cur += ch;
      }
    }
    row.push(cur);
    return row;
  });
}

function hasMandatoryColumn(headers) {
  return (headers[headers.length - 1] ?? "").toString().trim() === "Mandatory";
}

function parseMandatoryValue(cell) {
  const raw = (cell ?? "").toString().trim();
  return /^true$/i.test(raw);
}

/** Build list of dynamic column names between reserved columns and optional mandatory column. */
function computeDynamicHeaders(headers, reservedCount, hasMandatory) {
  const end = headers.length - (hasMandatory ? 1 : 0);
  return headers
    .slice(reservedCount, end)
    .map((h) => (h ? h.toString().trim() : ""))
    .filter((h) => h !== "");
}

/** Find the next row id starting value for an existing table. */
function getStartingNextId(existingTable) {
  if (existingTable.nextRowId) return existingTable.nextRowId;
  if (!existingTable.rows || existingTable.rows.length === 0) return 0;
  return Math.max(...existingTable.rows.map((r) => r.id || 0));
}

export function updateTableFromCSV(headers, dataRows, existingTable) {
  const hasMandatory = hasMandatoryColumn(headers);
  const dynamicHeaders = computeDynamicHeaders(headers, 3, hasMandatory);

  // Create dynamic columns using header labels
  const missingCols = dynamicHeaders
    .filter((col) => !existingTable.columns.find((c) => c.name === col))
    .map((name) => ({ name, validationRegex: "", validationText: "" }));

  const mergedColumns = [...existingTable.columns, ...missingCols];

  let nextId = getStartingNextId(existingTable);

  const newRows = dataRows.map((dr) => {
    nextId += 1;

    const row = {
      id: nextId,
      mandatory: false,
      name: "",
      max_spaces: "",
      min_size: ""
    };

    // positional mapping for first three columns
    if (dr.length > 0) row.name = (dr[0] ?? "").toString().trim();
    if (dr.length > 1) row.max_spaces = (dr[1] ?? "").toString().trim();
    if (dr.length > 2) row.min_size = (dr[2] ?? "").toString().trim();

    // dynamic columns
    for (let i = 3; i < headers.length - (hasMandatory ? 1 : 0); i++) {
      const headerName = headers[i] ? headers[i].toString().trim() : `col${i}`;
      row[headerName] = (dr[i] ?? "").toString().trim();
    }

    if (hasMandatory) {
      row.mandatory = parseMandatoryValue(dr[headers.length - 1]);
    }

    if (!row.name) row.name = `r${nextId}`;
    return row;
  });

  return {
    columns: mergedColumns,
    rows: newRows,
    nextRowId: nextId
  };
}