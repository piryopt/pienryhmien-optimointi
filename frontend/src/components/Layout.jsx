import Navbar from "./Navbar";
import Footer from "./Footer";
import configService from "../services/config";

const Layout = ({ children }) => {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Navbar />
      <main className="flex-shrink-0">
        <div className="container">
          <section className="content">{children}</section>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
