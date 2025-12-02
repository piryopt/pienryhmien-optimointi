import { Form, InputGroup } from "react-bootstrap";
import { useTranslation } from "react-i18next";
import { imagesBaseUrl } from "../utils/constants";

const GroupSearch = ({ searchTerm, setSearchTerm }) => {
  const { t } = useTranslation("answer");

  return (
    <InputGroup className="mb-2 group-search-input" style={{ width: "250px" }}>
      <Form.Control
        type="text"
        placeholder={t("Hae ryhmiä...")}
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="py-1"
      />
      <InputGroup.Text className="py-1 px-2">
        <img
          src={`${imagesBaseUrl}/search_black_24dp.svg`}
          className="d-inline-block align-text-middle"
          alt=""
        />
      </InputGroup.Text>
    </InputGroup>
  );
};

export default GroupSearch;
