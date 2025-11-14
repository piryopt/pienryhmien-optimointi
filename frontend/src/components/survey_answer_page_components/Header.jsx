import { imagesBaseUrl } from "../../utils/constants";

const Header = ({ surveyName }) => {
  return (
    <div className="header">
      <h1 className="answer-title">
        <img
          src={`${imagesBaseUrl}/assignment_white_36dp.svg`}
          alt=""
          className="assignment-icon"
        />
        {surveyName}
      </h1>
    </div>
  );
};

export default Header;
