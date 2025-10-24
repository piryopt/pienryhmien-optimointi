import {
  NotificationProvider,
  NotificationDisplay,
} from "../context/NotificationContext";
import Navbar from "./Navbar";
import Footer from "./Footer";
import configService from "../services/config";
import Notification from "./Notification";

const Layout = ({ children }) => {
  return (
    <div className="d-flex flex-column min-vh-100">
      <NotificationProvider>
        <Navbar />
        <NotificationDisplay />
        <main className="flex-shrink-0">
          <div className="container">
            <section className="content">{children}</section>
          </div>
        </main>
        <Footer />
      </NotificationProvider>
    </div>
  );
};

export default Layout;
