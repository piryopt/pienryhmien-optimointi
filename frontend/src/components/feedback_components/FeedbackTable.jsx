import Table from "../Table";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

/**
 * FeedbackTable
 * Props:
 *  - items: array of feedback rows
 *  - viewPathprefix: path prefix for the "view" link (default "/admintools/feedback")
 *
 * The table normalizes both server-returned objects and array rows.
 */
const FeedbackTable = ({
  items = [],
  viewPathPrefix = "/admintools/feedback"
}) => {
  const { t } = useTranslation();

  const columns = [
    { title: t("Otsikko") },
    { title: t("Palautteen tyyppi") },
    { title: t("Sähköposti") },
    { title: t("Toiminnot") }
  ];

  // Normalize a single item to { id, title, type, email, content, solved }
  const normalize = (it) => {
    if (!it) return {};
    if (Array.isArray(it)) {
      // legacy row shape used by server-rendered templates: [id, title, type, email, content, solved]
      return {
        id: it[0],
        title: it[1],
        type: it[2],
        email: it[3],
        content: it[4],
        solved: it[5]
      };
    }
    // assume object with named keys
    return {
      id: it.id ?? it[0],
      title: it.title ?? it[1],
      type: it.type ?? it[2],
      email: it.email ?? it[3],
      content: it.content ?? it[4],
      solved: it.solved ?? it[5]
    };
  };

  const renderRow = (rawItem) => {
    const item = normalize(rawItem);
    return (
      <tr key={item.id ?? JSON.stringify(item)}>
        <td>{item.title}</td>
        <td>{item.type}</td>
        <td>{item.email || "-"}</td>
        <td>
          <Link to={`${viewPathPrefix}/${item.id}`}>{t("Tarkastele")}</Link>
        </td>
      </tr>
    );
  };

  return (
    <>
      <style>{`
        /* hide header icons for the feedback table only */
        .feedback-table thead img { display: none !important }
      `}</style>
      <Table
        columns={columns}
        data={items}
        renderRow={renderRow}
        className="table table-striped feedback-table"
      />
    </>
  );
};

export default FeedbackTable;
