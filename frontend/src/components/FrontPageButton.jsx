import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

const FrontPageButton = ({
  path,
  imgSrc,
  mainText,
  additionalText,
  topRightText,
  additionalVars
}) => {
  const { t } = useTranslation("front");

  return (
    <Link
      to={path}
      className="list-group-item list-group-item-action"
      style={{ borderRadius: "12px" }}
    >
      <div className="d-flex w-100">
        <div className="d-flex w-100">
          <img
            src={imgSrc}
            alt=""
            width="34"
            height="30"
            className=""
            style={{ marginRight: "8px" }}
          />
          <p style={{ fontSize: "130%" }}>{t(mainText, additionalVars)}</p>
        </div>

        {topRightText && (
          <small className="text-muted text-nowrap">
            {t(topRightText, additionalVars)}
          </small>
        )}
      </div>
      <small className="text-muted">{t(additionalText, additionalVars)}</small>
    </Link>
  );
};

export default FrontPageButton;
