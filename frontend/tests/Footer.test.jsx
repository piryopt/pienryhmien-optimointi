import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import Footer from "../src/components/Footer";

describe("<Footer />", () => {
  beforeEach(() => {
    render(
      <MemoryRouter>
        <Footer />
      </MemoryRouter>
    );
  });

  test("renders footer links", () => {
    screen.getByText("UKK");
    screen.getByText("Anna palautetta");
    screen.getByText("Tietosuojaseloste");
  });
});
