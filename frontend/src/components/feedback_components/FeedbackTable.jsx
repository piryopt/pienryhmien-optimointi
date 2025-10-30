import Table from "../Table"
import { Link } from "react-router-dom"
import { useTranslation } from "react-i18next"

const FeedbackTable = ({ items }) => {
  const { t } = useTranslation()

  const columns = [
    { title: t("Otsikko") },
    { title: t("Palautteen tyyppi") },
    { title: t("Sähköposti") },
    { title: t("Tarkastele")}
  ]

  const renderRow = (item) => {
    return (
      <tr key={item.id}>
        <td>{item.title}</td>
        <td>{item.type}</td>
        <td>{item.email}</td>
        <td>
          <Link to={`/admintools/feedback/${item.id}`}>{t("Tarkastele")}</Link>
        </td>
      </tr>
    )
  }

  return <Table columns={columns} data={items} renderRow={renderRow} />
}

export default FeedbackTable