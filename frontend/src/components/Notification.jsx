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
    backgroundColor: "lightgrey",
    margin: "10px",
    padding: "10px",
    border: "2px solid",
    borderColor: notification.type === "success" ? "green" : "red",
    borderRadius: "5px",
  };
  return <div style={style}>{notification.message}</div>;
};

export default Notification;
