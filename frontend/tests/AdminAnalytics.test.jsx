import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import AdminAnalytics from "../src/pages/admintools/AdminAnalytics.jsx";
import { AuthProvider } from "../src/context/AuthProvider";
import adminService from "../src/services/admin";

// Mock the survey service
vi.mock("../src/services/admin", () => ({
  default: {
    fetchAnalytics: vi.fn()
  }
}));

describe("<AdminAnalytics />", () => {
  beforeEach(() => {
    adminService.fetchAnalytics.mockResolvedValue({
      success: true,
      data: {
        total_surveys: 15,
        active_surveys: 2,
        total_teachers: 3,
        total_students: 4,
        total_responses: 45
      }
    });

    render(
      <MemoryRouter>
        <AuthProvider>
          <AdminAnalytics />
        </AuthProvider>
      </MemoryRouter>
    );
  });

  test("render admin analytics table", async () => {
    await waitFor(() => {
      screen.getByText("Jakajassa luodut kyselyt");
      screen.getByText("Kaikki käynnissä olevat kyselyt");
      screen.getByText("Rekisteröityneet opettajat");
      screen.getByText("Rekisteröityneet opiskelijat");
      screen.getByText("Vastauksia luotu");
    });
  });

  test("render admin analytics stats", async () => {
    await waitFor(() => {
      screen.getByRole("row", { name: /15 2 3 4 45/i });
    });
  });
});
