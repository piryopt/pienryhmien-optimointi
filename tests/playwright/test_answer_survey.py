from pathlib import Path
from playwright.sync_api import Page, expect
from .playwright_tools import login, mouse_dnd

TEST_FILES_PATH = Path(__file__).parent / ".." / "test_files"


def test_go_to_all_surveys_page(setup_db, page: Page):
    """
    Test that the user can go to the all surveys page from the front page
    """
    login(page, "robottiTeacher", "train")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    expect(page.get_by_text("Kyselyn tila")).to_be_visible()
    expect(page.get_by_text("Toiminnot")).to_be_visible()


def test_survey_more_info_works(setup_db, page: Page, create_survey_with_csv_file):
    """
    Test that if a survey choice has additional info, it is displayed when clicked and hidden when clicked again
    """
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Päiväkoti valinta").click()
    page.get_by_text("Päiväkoti Floora").click()
    expect(page.get_by_text("Syyriankatu 1").first).to_be_visible()
    expect(page.get_by_text("00560").first).to_be_visible()
    page.get_by_text("Päiväkoti Toivo").click()
    expect(page.get_by_text("Apteekkarinraitti 3").first).to_be_visible()
    expect(page.get_by_text("00790").first).to_be_visible()


def test_answer_survey(setup_db, page: Page, create_survey_with_csv_file):
    """
    Test that a user can answer a created survey
    """
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Päiväkoti valinta").click()

    page.get_by_test_id("submit-button").click()
    expect(page.get_by_text("Tallennus epäonnistui. Valitse vähintään 4")).to_be_visible()

    expect(page.get_by_text("Päiväkoti valinta").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Floora").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Toivo").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Kotikallio").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Nalli").first).to_be_visible()

    mouse_dnd(page, "Päiväkoti Toivo", '[data-rfd-droppable-id="good"]')
    mouse_dnd(page, "Päiväkoti Floora", '[data-rfd-droppable-id="good"]')
    mouse_dnd(page, "Päiväkoti Kotikallio", '[data-rfd-droppable-id="good"]')
    mouse_dnd(page, "Päiväkoti Nalli", '[data-rfd-droppable-id="good"]')

    # Makes sure that last item has been let go
    page.wait_for_timeout(1000)

    items = page.locator('[data-rfd-droppable-id="good"] >> [data-rfd-draggable-id]')
    assert items.count() == 4

    page.get_by_test_id("submit-button").click()
    expect(page.get_by_text("Tallennus onnistui.")).to_be_visible()


def test_delete_survey_answer(setup_db, page: Page, create_survey_with_csv_file):
    """
    Test that a user can delete their submitted ranking
    """

    # First we answer survey
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Päiväkoti valinta").click()

    page.get_by_test_id("submit-button").click()
    expect(page.get_by_text("Tallennus epäonnistui. Valitse vähintään 4")).to_be_visible()

    expect(page.get_by_text("Päiväkoti valinta").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Toivo").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Floora").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Kotikallio").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Nalli").first).to_be_visible()

    mouse_dnd(page, "Päiväkoti Floora", '[data-rfd-droppable-id="good"]')
    mouse_dnd(page, "Päiväkoti Toivo", '[data-rfd-droppable-id="good"]')
    mouse_dnd(page, "Päiväkoti Kotikallio", '[data-rfd-droppable-id="good"]')
    mouse_dnd(page, "Päiväkoti Nalli", '[data-rfd-droppable-id="good"]')

    # Makes sure that last item has been let go
    page.wait_for_timeout(1000)

    items = page.locator('[data-rfd-droppable-id="good"] >> [data-rfd-draggable-id]')
    assert items.count() == 4

    page.get_by_test_id("submit-button").click()
    expect(page.get_by_text("Tallennus onnistui.")).to_be_visible()

    page.go_back()

    # Delete answers
    page.get_by_role("link", name="Päiväkoti valinta").click()
    page.get_by_test_id("delete-button").click()
    expect(page.get_by_text("Valinnat poistettu")).to_be_visible()
