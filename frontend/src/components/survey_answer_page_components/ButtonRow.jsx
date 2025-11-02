import Button from 'react-bootstrap/Button';

const ButtonRow = ({ handleSubmit, handleDelete, existing }) => {
  return (
    <div className="submit-row">
      <Button variant="success" className="submit-btn" onClick={handleSubmit}>
        Lähetä valinnat
      </Button>
      { existing &&
        <Button variant="danger" className="submit-btn" onClick={handleDelete} style={{marginLeft: '15px'}}>
          Poista valinnat
        </Button>
      }
    </div>
  );
}

export default ButtonRow;