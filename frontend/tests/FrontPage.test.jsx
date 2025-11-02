import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import FrontPage from "../src/pages/FrontPage";

describe("<FrontPage />", () => {
  beforeEach(() => {
    render(
      <MemoryRouter>
        <FrontPage />
      </MemoryRouter>
    );
  });

  test("render front page buttons", () => {
    screen.getByText("Luo uusi kysely");
    screen.getByText("Näytä vanhat kyselyt");
    screen.getByText("Luo uusi monivaiheinen kysely");
  });
});
