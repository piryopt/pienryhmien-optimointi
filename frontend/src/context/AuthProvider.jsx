import React, { createContext, useContext, useEffect, useState } from "react";
import { baseUrl } from "../utils/constants";
import csrfService from "../services/csrf";
import configService from "../services/config";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [debug, setDebug] = useState(null);

  const refreshSession = async () => {
    try {
      const res = await fetch(`${baseUrl}/session`, {
        credentials: "include"
      });
      const data = await res.json();
      setUser(data.logged_in ? data : false);
      return data;
    } catch (err) {
      console.error("refreshSession failed", err);
      setUser(false);
      return { logged_in: false };
    }
  };

  useEffect(() => {
    (async () => {
      try {
        const flag = await configService.fetchDebugFlag();
        setDebug(flag);
      } catch (e) {
        console.error("fetchDebugFlag failed", e);
        setDebug(false);
      }

      try {
        await refreshSession();
      } catch (e) {
        console.error("refreshSession retries failed", e);
      }

      setLoading(false);
    })();
  }, []);

  const login = async ({ username, password }) => {
    const csrfToken = await csrfService.fetchCsrfToken();
    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);

    const res = await fetch(`${baseUrl}/auth/login`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken
      },
      body: body.toString()
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ message: res.statusText }));
      throw new Error(err?.message || "Login failed");
    }

    await refreshSession();
  };

  const logout = async () => {
    if (debug) {
      const csrf = await csrfService.fetchCsrfToken();
      await fetch(`${baseUrl}/logout`, {
        method: "POST",
        credentials: "include",
        headers: { "X-CSRFToken": csrf, "Content-Type": "application/json" }
      });
      await refreshSession();
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, loading, debug, login, logout, refreshSession }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
