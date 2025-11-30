from pathlib import Path
from playwright.sync_api import Page, expect
from .playwright_tools import login

TEST_FILES_PATH = Path(__file__).parent / ".." / "test_files"


def test_go_to_create_multistage_survey_page(setup_db, page: Page):
    """
    Test that the user can go to the create new multistage survey page from the front page
    """
    login(page, "robottiTeacher", "sleep")
    page.get_by_role(
        "link",
        name="Luo uusi monivaiheinen kysely",
    ).click()
    expect(page.get_by_text("Rajoita osallistumiskertoja")).to_be_visible()
    expect(
        page.get_by_role(
            "button",
            name="Lisää vaihe",
        )
    ).to_be_visible()


def test_creating_multistage_survey_without_stages(setup_db, page: Page):
    """
    Test that multistage survey creation fail if you don't add any stages
    """
    login(page, "robottiTeacher", "sleep")
    page.get_by_role(
        "link",
        name="Luo uusi monivaiheinen kysely",
    ).click()
    page.get_by_test_id("groupname").fill("Eeppinen monivaiheinen kysely")
    page.locator("#end-date").fill("31.05.2029")
    page.locator("#endtime").select_option("12:00")
    page.get_by_test_id("survey-information").fill("Katotaan tyhjillä vaiheilla")

    page.get_by_role(
        "button",
        name="Luo kysely",
    ).click()
    expect(page.get_by_text("Lisää ainakin yksi vaihe")).to_be_visible()
