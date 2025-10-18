import Navbar from "./Navbar";

const Layout = ({ children }) => (
  <div className="d-flex flex-column min-vh-100">
    <Navbar />
    <main className="flex-shrink-0">
      <div className="container">
        <section className="content">
          {children}
        </section>
      </div>
    </main>
  </div>
);

export default Layout;
