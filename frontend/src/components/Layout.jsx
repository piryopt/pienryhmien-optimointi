import Navbar from "./Navbar";

const Layout = ({ children }) => {
  return (
    <div>
      <Navbar />
      <main className="flex-shrink-0 container">
        <div className="container">
          <section className="content">
            {children}
          </section>
        </div>
      </main>
    </div>
  );
};

export default Layout
