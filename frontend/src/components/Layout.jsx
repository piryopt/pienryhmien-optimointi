import Navbar from "./Navbar";
import Footer from "./Footer";

const Layout = ({ children }) => (
  <div className="d-flex flex-column min-vh-100">
    <Navbar />
    <main className="flex-shrink-0 container">{children}</main>
    <Footer />
  </div>
);

export default Layout;
