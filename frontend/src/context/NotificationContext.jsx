import React, { createContext, useContext, useState } from "react";
import Notification from "../components/Notification";

const NotificationContext = createContext();
export const useNotification = () => useContext(NotificationContext);

export const NotificationProvider = ({ children }) => {
  const [notification, setNotification] = useState(null);
  const showNotification = (message, type = "success") =>
    setNotification({ message, type });
  const hideNotification = () => setNotification(null);

  return (
    <NotificationContext.Provider
      value={{
        notification,
        showNotification,
        hideNotification,
        setNotification
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};

export const NotificationDisplay = () => {
  const { notification, hideNotification } = useNotification();
  return (
    <Notification
      notification={notification}
      onClose={hideNotification}
    ></Notification>
  );
};
