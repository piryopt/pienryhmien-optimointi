import { useTranslation } from "react-i18next";
import { imagesBaseUrl } from "../../utils/constants";

const Header = () => {
  const { t } = useTranslation();
  return (
    <h1 className="page-title">
      <img
        src={`${imagesBaseUrl}/note_add_white_36dp.svg`}
        alt="note add logo"
        className="d-inline-block align-text-middle"
      />
      {t("Luo uusi kysely")}
    </h1>
  );
};

export default Header;
