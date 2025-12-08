import { afterEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn()
};
global.localStorage = localStorageMock;

// Mock fetch for session and config endpoints
global.fetch = vi.fn((url) => {
  if (url.includes("/session")) {
    return Promise.resolve({
      ok: true,
      json: () =>
        Promise.resolve({
          logged_in: true,
          user: "test_user",
          admin: false
        })
    });
  }
  if (url.includes("/config")) {
    return Promise.resolve({
      ok: true,
      json: () =>
        Promise.resolve({
          debug: true
        })
    });
  }
  return Promise.reject(new Error("Unknown fetch: " + url));
});

// Mock the useTranslation hook
vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key) => key,
    i18n: {
      language: "fi",
      changeLanguage: vi.fn()
    }
  })
}));

// Mock the CSRF service
vi.mock("/src/services/csrf", () => ({
  default: {
    fetchCsrfToken: vi.fn().mockResolvedValue("test-csrf-token")
  }
}));

// Mock the notification context
vi.mock("/src/context/NotificationContext", () => ({
  useNotification: vi.fn(() => ({
    notification: null,
    showNotification: vi.fn(),
    hideNotification: vi.fn(),
    setNotification: vi.fn()
  }))
}));
