import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import FrontPage from "../src/pages/FrontPage";
import { AuthProvider } from "../src/context/AuthProvider";
import surveyService from "../src/services/surveys";

// Mock the survey service
vi.mock("../src/services/surveys", () => ({
  default: {
    getFrontPageData: vi.fn()
  }
}));

describe("<FrontPage />", () => {
  beforeEach(() => {
    surveyService.getFrontPageData.mockResolvedValue({
      createdSurveys: 0,
      activeSurveys: [],
      trashCount: 0
    });

    render(
      <MemoryRouter>
        <AuthProvider>
          <FrontPage />
        </AuthProvider>
      </MemoryRouter>
    );
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  test("render front page buttons", async () => {
    await waitFor(() => {
      screen.getByText("Luo uusi kysely");
      screen.getByText("Näytä vanhat kyselyt");
      screen.getByText("Luo uusi monivaiheinen kysely");
      screen.getByText("Roskakori");
    });
  });

  test("fetch front page data on load", async () => {
    await waitFor(() => {
      expect(surveyService.getFrontPageData).toHaveBeenCalledTimes(1);
    });
  });

  test("render front page with surveys", async () => {
    // Override the mock for this test only
    surveyService.getFrontPageData.mockResolvedValueOnce({
      createdSurveys: 5,
      activeSurveys: [
        {
          id: 1,
          surveyname: "Test Survey",
          is_multistage: false,
          time_end: "2026-12-31",
          response_count: 10
        },
        {
          id: 2,
          surveyname: "Mega survey",
          is_multistage: true,
          time_end: "2026-12-31",
          response_count: 150
        }
      ],
      trashCount: 2
    });

    render(
      <MemoryRouter>
        <AuthProvider>
          <FrontPage />
        </AuthProvider>
      </MemoryRouter>
    );

    await waitFor(() => {
      screen.getByText("Test Survey");
      screen.getByText("Mega survey");
    });
  });
});
