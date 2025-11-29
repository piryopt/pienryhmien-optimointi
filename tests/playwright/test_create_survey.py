from pathlib import Path
from playwright.sync_api import Page, expect
from .playwright_tools import login, mouse_dnd

TEST_FILES_PATH = Path(__file__).parent / ".." / "test_files"


def test_go_to_create_survey_page(setup_db, page: Page):
    """
    Test that the user can go to the create new survey page from the front page
    """
    login(page, "robottiTeacher", "sleep")
    page.get_by_role(
        "link",
        name="Luo uusi kysely",
    ).click()
    expect(page.get_by_text("Kyselyn nimi")).to_be_visible()
    expect(page.get_by_text("Tähän voit antaa kuvauksen kyselystä ja ohjeita siihen vastaamiseen.")).to_be_visible()


def test_create_new_survey_with_csv_file(setup_db, page: Page):
    """
    Test that the user is able to create a new survey with a pre-made CSV file
    """
    page.on("console", lambda msg: print(f"[BROWSER LOG] {msg.type}: {msg.text}"))

    login(page, "robottiTeacher", "RoboCop")
    page.get_by_role(
        "link",
        name="Luo uusi kysely Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta",
    ).click()
    page.get_by_test_id("groupname").fill("Päiväkoti valinta")
    page.locator("#end-date").fill("31.08.2029")
    page.locator("#endtime").select_option("12:00")
    page.get_by_test_id("survey-information").fill("Valitse mihin päiväkotiin haluat sijoittaa itsesi")

    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Tuo valinnat CSV-tiedostosta").click()
    file_chooser = fc_info.value
    file_chooser.set_files(str(TEST_FILES_PATH) + "/test_survey2.csv")

    input_locator = page.locator("#choiceTable tr").nth(0).locator("td").nth(1).locator("input")
    expect(input_locator).to_have_value("Päiväkoti Toivo")

    input_locator = page.locator("#choiceTable tr").nth(3).locator("td").nth(4).locator("input")
    expect(input_locator).to_have_value("Nallitie 3")

    page.get_by_test_id("create-button").click()
    expect(page.get_by_text("Uusi kysely luotu!")).to_be_visible()


def test_create_new_survey(setup_db, page: Page):
    """
    Test that the user is able to create a new survey
    """
    page.on("console", lambda msg: print(f"Console [{msg.type}]: {msg.text}"))

    login(page, "robottiTeacher", "abuse gear")
    page.get_by_role(
        "link",
        name="Luo uusi kysely Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta",
    ).click()

    page.get_by_test_id("groupname").fill("Menaces")
    page.locator("#end-date").fill("31.08.2029")
    page.locator("#endtime").select_option("22:00")
    page.get_by_test_id("survey-information").fill("Absolute menaces to society")

    page.locator("#choiceTable tr").nth(0).locator("td").nth(1).click()
    page.keyboard.type("Vegeta")
    page.keyboard.press("Tab")
    page.keyboard.type("5")
    page.keyboard.press("Tab")
    page.keyboard.type("0")
    page.locator("xpath=//*[@id='add-column-header']").click()
    page.keyboard.type("Quotes")
    page.keyboard.press("Enter")
    page.locator("#choiceTable tr").nth(0).locator("td").nth(4).click()
    page.keyboard.type("Trespass into the domain of the Gods!")

    page.get_by_test_id("add-choice-button").click()

    page.locator("#choiceTable tr").nth(1).locator("td").nth(1).click()
    page.keyboard.type("Barou")
    page.keyboard.press("Tab")
    page.keyboard.type("5")
    page.keyboard.press("Tab")
    page.keyboard.type("0")
    page.keyboard.press("Tab")
    page.keyboard.type("Talent without hard work is nothing.")

    page.get_by_test_id("add-choice-button").click()

    page.locator("#choiceTable tr").nth(2).locator("td").nth(1).click()
    page.keyboard.type("Isagi")
    page.keyboard.press("Tab")
    page.keyboard.type("5")
    page.keyboard.press("Tab")
    page.keyboard.type("0")
    page.keyboard.press("Tab")
    page.keyboard.type("How does it feel to be the clown of my story?")
    page.wait_for_timeout(500)
    page.get_by_test_id("create-button").click()
    expect(page.get_by_text("Uusi kysely luotu!")).to_be_visible()


def test_mandatory_groups_get_filled_using_csv_file(setup_db, page: Page):
    login(page, "robottiTeacher", "sleep")
    page.get_by_role("link", name="Luo uusi kysely").click()
    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Tuo valinnat CSV-tiedostosta").click()
    file_chooser = fc_info.value
    file_chooser.set_files(str(TEST_FILES_PATH) + "/test_survey3.csv")
    page.wait_for_selector("table")
    rows = page.locator("table tbody tr")
    first_checkbox = rows.nth(0).locator("input[type='checkbox']")
    second_checkbox = rows.nth(1).locator("input[type='checkbox']")
    fourth_checkbox = rows.nth(3).locator("input[type='checkbox']")
    assert first_checkbox.is_checked()
    assert not second_checkbox.is_checked()
    assert fourth_checkbox.is_checked()
