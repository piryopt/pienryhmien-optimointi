import hyLogo from "../static/images/hy_logo.svg";

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark">
      <div className="container-fluid">
        <a className="navbar-brand" href="/">
          <img
            src={hyLogo}
            alt=""
            width="34"
            height="30"
            className="d-inline-block align-text-top"
          />
          Jakaja
        </a>
        <div className="collapse navbar-collapse" id="navbarNav">
          <a className="nav-link" href="#">
            <small>Tilastot</small>
          </a>
          <a className="nav-link" href="#">
            <small>Palaute</small>
          </a>
          <a className="nav-link" href="#">
            <small>Aktiiviset kyselyt</small>
          </a>
        </div>
        <div className="d-flex">
          <div className="dropdown">
            <button
              className="btn dropdown btn-sm"
              type="button"
              id="dropdownMenuButton1"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            ></button>
            <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
              <li>
                <a className="dropdown-item" href="#">
                  <small>Kirjaudu ulos</small>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
