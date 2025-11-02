import assignmentIcon from '/images/assignment_white_36dp.svg';

const Header = ({ surveyName }) => {
  return (
    <div className="header">
      <h1 className="answer-title">
        <img src={assignmentIcon} alt="" className="assignment-icon" />
        {surveyName}
      </h1>
    </div>
  );
}

export default Header;
