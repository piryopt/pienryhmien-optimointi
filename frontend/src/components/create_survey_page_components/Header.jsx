import noteAddLogo from "/images/note_add_white_36dp.svg";
import { useTranslation } from "react-i18next";

const Header = () => {
  const { t } = useTranslation();
  return (
    <h1 className="page-title">
      <img
        src={noteAddLogo}
        alt="note add logo"
        className="d-inline-block align-text-middle"
      />
      {t("Luo uusi kysely")}
    </h1>
  );
};

export default Header;
