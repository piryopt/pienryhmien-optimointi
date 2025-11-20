import { useEffect } from "react";

const Notification = ({ notification, onClose }) => {
  useEffect(() => {
    if (!notification) return;
    const timer = setTimeout(() => {
      if (onClose) onClose();
    }, 5000);

    return () => clearTimeout(timer);
  }, [notification, onClose]);

  if (!notification) {
    return null;
  }

  const style = {
    bottom: 0,
    zIndex: 10,
    background: notification.type === "success" ? "green" : "red",
    height: "50px",
    width: "100%",
    margin: "0 auto",
    color: "rgb(255, 255, 255)",
    opacity: 0.9,
    textAlign: "center",
    paddingTop: "10px",
    position: "fixed",
    WebkitBoxShadow: "0px 1px 0px rgba(0, 0, 0, 0.2)"
  };

  return <div style={style}>{notification.message}</div>;
};

export default Notification;
