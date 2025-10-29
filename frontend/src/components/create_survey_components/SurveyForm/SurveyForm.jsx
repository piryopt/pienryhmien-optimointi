import { useEffect, useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";
import ChoiceTable from "../ChoiceTable";
import { isoToDDMM, padTimeHHMM } from "./helpers";
import { validateSurvey } from "./validation";

const SurveyForm = () => {
  const { t } = useTranslation();
  const nextRowId = useRef(1);

  const [groupname, setGroupname] = useState("");
  const [surveyInformation, setSurveyInformation] = useState("");
  const [endDate, setEndDate] = useState("");
  const [endTime, setEndTime] = useState("23:59");
  const [minChoicesMode, setMinChoicesMode] = useState("all");
  const [minChoices, setMinChoices] = useState("");
  const [denyChoicesMode, setDenyChoicesMode] = useState("no");
  const [deniedChoicesCount, setDeniedChoicesCount] = useState("");
  const [allowSearchVisibility, setAllowSearchVisibility] = useState(true);

  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([{ id: 1, mandatory: false, name: "", max_spaces: "", min_size: "" }]);
  const [selectAllMandatory, setSelectAllMandatory] = useState(false);

  const [errors, setErrors] = useState([]);
  const [saving, setSaving] = useState(false);
  const [successMsg, setSuccessMsg] = useState(null);

  useEffect(() => {
    setRows((r) => r.map((x) => ({ ...x, mandatory: selectAllMandatory })));
  }, [selectAllMandatory]);

  const addRow = () => {
    const id = ++nextRowId.current;
    const extra = columns.reduce((a, c) => ({ ...a, [c.name]: "" }), {});
    setRows((r) => [...r, { id, mandatory: false, name: "", max_spaces: "", min_size: "", ...extra }]);
  };

  const deleteRow = (id) => setRows((r) => r.filter((x) => x.id !== id));
  const updateCell = (id, key, value) => setRows((r) => r.map((row) => (row.id === id ? { ...row, [key]: value } : row)));

  const addColumn = (name) => {
    if (!name || columns.find((c) => c.name === name)) return;
    setColumns((c) => [...c, { name, validationRegex: "", validationText: "" }]);
    setRows((rs) => rs.map((r) => ({ ...r, [name]: "" })));
  };

  const removeColumn = (name) => {
    setColumns((c) => c.filter((x) => x.name !== name));
    setRows((rs) =>
      rs.map((r) => {
        const copy = { ...r };
        delete copy[name];
        return copy;
      })
    );
  };

  const parseCSV = (text) => {
    const rows = [];
    let cur = "", inQuotes = false, row = [];

    for (let i = 0; i < text.length; i++) {
        const ch = text[i];
        if (ch === '"') {
        if (inQuotes && text[i + 1] === '"') {
            cur += '"';
            i++;
        } else {
            inQuotes = !inQuotes;
        }
        continue;
        }
        if (ch === "," && !inQuotes) {
            row.push(cur);
            cur = "";
            continue;
        }
        if ((ch === "\n" || ch === "\r") && !inQuotes) {
            if (ch === "\r" && text[i + 1] === "\n") i++;
            row.push(cur);
            rows.push(row);
            row = [];
            cur = "";
            continue;
        }
        cur += ch;
    }

    if (cur !== "" || row.length) {
        row.push(cur);
        rows.push(row);
    }
    return rows;
    };

    const importCSV = (file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
        const text = e.target.result;
        const parsed = parseCSV(text);
        if (!parsed.length) return;

        const hdrRaw = parsed[0].map((h) => (h === undefined || h === null ? "" : String(h).trim()));
        if (hdrRaw.length < 3) {
            while (hdrRaw.length < 3) hdrRaw.push("");
        }

        const body = parsed.slice(1).filter((r) => r.some((c) => c !== ""));

        const varCols = hdrRaw.slice(3).map((h) => h || "");
        const normalizedVarCols = varCols
            .map((n, i) => (n && n.length ? n : `column_${i + 1}`))
            .filter((v, i, arr) => arr.indexOf(v) === i);

        setColumns(normalizedVarCols.map((n) => ({ name: n, validationRegex: "", validationText: "" })));

        const mapped = body.map((r) => {
            const id = nextRowId.current++;
            const base = {
            id,
            mandatory: !!( (r[0] && r[0].toLowerCase && r[0].toLowerCase() === "mandatory") ? false : false ),
            name: (r[0] !== undefined ? String(r[0]).trim() : ""),
            max_spaces: (r[1] !== undefined ? String(r[1]).trim() : ""),
            min_size: (r[2] !== undefined ? String(r[2]).trim() : ""),
            };
            normalizedVarCols.forEach((colName, idx) => {
            base[colName] = r[3 + idx] !== undefined ? String(r[3 + idx]).trim() : "";
            });
            return base;
        });

        setRows(mapped.length ? mapped : [{ id: nextRowId.current++, mandatory: false, name: "", max_spaces: "", min_size: "" }]);
        };
        reader.readAsText(file, "utf-8");
    };

  const createSurvey = async () => {
    const errs = validateSurvey(t, groupname, endDate, rows, columns);
    if (errs.length) {
      setErrors(errs);
      return;
    }

    setSaving(true);
    setErrors([]);
    setSuccessMsg(null);

    const payload = {
      surveyGroupname: groupname,
      surveyInformation: surveyInformation,
      enddate: endDate,
      endtime: padTimeHHMM(endTime),
      minchoices: minChoicesMode === "all" ? rows.length : Number(minChoices || rows.length),
      allowedDeniedChoices: denyChoicesMode === "no" ? 0 : Number(deniedChoicesCount || 0),
      allowSearchVisibility,
      choices: rows.map((r) => {
        const base = {
          mandatory: !!r.mandatory,
          name: r.name,
          max_spaces: Number(r.max_spaces) || 0,
          min_size: Number(r.min_size) || 0,
        };
        columns.forEach((c) => (base[c.name] = r[c.name] ?? ""));
        return base;
      }),
    };

    try {
      const res = await fetch("/surveys/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const json = await res.json();

      if (!res.ok || json.status !== "1") {
        setErrors([json.msg || t("Kyselyn luonti epäonnistui")]);
      } else {
        setSuccessMsg(json.msg || t("Kysely luotu"));
        window.location.href = "/";
      }
    } catch (e) {
      setErrors([String(e)]);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      {errors.length > 0 && (
        <div style={{ color: "crimson", marginBottom: 8 }}>
          <ul>
            {errors.map((err, i) => <li key={i}>{err}</li>)}
          </ul>
        </div>
      )}
      {successMsg && <div style={{ color: "green" }}>{successMsg}</div>}

      <section>
        <h2>{t("Kyselyn nimi")}</h2>
        <input value={groupname} onChange={(e) => setGroupname(e.target.value)} />
      </section>

      <section>
        <h2>{t("Vastausaika")}</h2>
        <p>{t("Vastausaika määrittää aikavälin, jolloin kyselyyn on mahdollista vastata.")}</p>
        <input
          type="date"
          onChange={(e) => setEndDate(isoToDDMM(e.target.value))}
          value={
            endDate
              ? (() => {
                  const p = endDate.split(".");
                  return p.length === 3 ? `${p[2]}-${p[1]}-${p[0]}` : "";
                })()
              : ""
          }
        />
        <input type="time" value={endTime} onChange={(e) => setEndTime(e.target.value)} />
      </section>

      <section>
        <h2>{t("Kyselyn kuvaus")}</h2>
        <p>{t("Tähän voit antaa kuvauksen kyselystä ja ohjeita siihen vastaamiseen. \
    Kuvausteksti näytetään vastaajalle kyselyn yhteydessä.")}</p>
        <textarea value={surveyInformation} onChange={(e) => setSurveyInformation(e.target.value)} />
      </section>

      <section>
        <h2>{t("Vaaditaanko kaikkien ryhmien järjestämistä?")}</h2>
        <p>{t("Suositellaan, että vaaditaan kaikkien ryhmien järjestämistä ellei niitä ole suuri määrä (>10)")}</p>
        <div>
          <label>
            <input type="radio" name="minchoices" checked={minChoicesMode === "all"} onChange={() => setMinChoicesMode("all")} /> {t("Kyllä")}
          </label>
          <label style={{ marginLeft: 12 }}>
            <input type="radio" name="minchoices" checked={minChoicesMode === "custom"} onChange={() => setMinChoicesMode("custom")} /> {t("Ei")}
          </label>
          {minChoicesMode === "custom" && (
            <div>
                <p>{t("Priorisoitujen ryhmien vähimmäismäärä")}</p>
                <input value={minChoices} onChange={(e) => setMinChoices(e.target.value)} />
            </div>
          )}
        </div>

        <div>
          <h2>{t("Sallitaanko valintojen kieltäminen?")}</h2>
          <label>
            <input type="radio" name="denychoices" checked={denyChoicesMode === "yes"} onChange={() => setDenyChoicesMode("yes")} /> {t("Kyllä")}
          </label>
          <label style={{ marginLeft: 12 }}>
            <input type="radio" name="denychoices" checked={denyChoicesMode === "no"} onChange={() => setDenyChoicesMode("no")} /> {t("Ei")}
          </label>
          {denyChoicesMode === "yes" && (
            <div>
                <p>{t("Sallittu kiellettyjen ryhmien määrä")}</p>
                <input value={deniedChoicesCount} onChange={(e) => setDeniedChoicesCount(e.target.value)} />
            </div>
          )}
        </div>

        <div>
          <h2>{t("Näytetäänkö vastaajalle hakupalkki?")}</h2>
          <p>{t("Hakupalkin avulla kyselyyn vastaaja voi suodattaa näkemiään vaihtoehtoja sen nimen ja vaihtoehtojen perusteella. Suositeltavaa sallia kyselyille, joissa on runsaasti ei-pakollisia vaihtoehtoja, ja vastaavasti kieltää pakollisia vaihtoehtoja sisältävälle tai pienelle kyselylle.")}</p>
          <label><input type="radio" checked={allowSearchVisibility} onChange={() => setAllowSearchVisibility(true)} /> {t("Kyllä")}</label>
          <label style={{ marginLeft: 8 }}><input type="radio" checked={!allowSearchVisibility} onChange={() => setAllowSearchVisibility(false)} /> {t("Ei")}</label>
        </div>
      </section>

      <section>
        <h2>{t("Priorisoitavat ryhmät")}</h2>
        <p>{t("Syötä ryhmät, jotka kyselyyn vastaaja voi asettaa mielekkyysjärjestykseen. Anna kullekkin ryhmälle myös sen enimmäiskoko. Halutessasi voit lisätä lisätietoa kohteesta omiin sarakkeisiinsa. Sarakkeen voit luoda painamalla '+ Lisää tietokenttä'.")}</p>
        <Link to="/csv-instructions" className="text-muted">{t("CSV-ohje")}</Link>
        <div style={{ marginBottom: 8 }}>
          <input type="file" accept=".csv" onChange={(e) => { if (e.target.files && e.target.files[0]) importCSV(e.target.files[0]); }} />
        </div>
        <p>{t("Jos haluat, ettei jonkun tietyn sarakkeen tieto näy vastausvaiheessa opiskelijoille, laita sen sarakkeen nimen viimeiseksi merkiksi *.")}</p>
        <p>{t("Jos ryhmän minimikoolla ei ole väliä, syötä 0. Pakollisen ryhmän mimimikoko ei voi olla 0.")}</p>
        <p>{t("HUOM! Alle minimikoon jäävät ryhmät jätetään pois jaosta. Jos haluat, että tietty ryhmä toteutuu varmasti, rastita ryhmän vasemmalla puolella oleva laatikko.")}</p>

        <ChoiceTable
          columns={columns}
          rows={rows}
          addRow={addRow}
          deleteRow={deleteRow}
          addColumn={addColumn}
          removeColumn={removeColumn}
          updateCell={updateCell}
          selectAllMandatory={selectAllMandatory}
          setSelectAllMandatory={setSelectAllMandatory}
        />
      </section>

      <section>
        <button class="new-row-input btn btn-secondary" disabled={saving} onClick={createSurvey}>{saving ? t("Luodaan…") : t("Luo kysely")}</button>
      </section>
    </div>
  );
};

export default SurveyForm;
