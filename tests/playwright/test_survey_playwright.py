from pathlib import Path
import re
from playwright.sync_api import Page, expect
from .playwright_tools import login

TEST_FILES_PATH = Path(__file__).parent / ".." / "test_files"


def test_login(setup_db, page: Page):
    """
    Test that mock ad login works. After login the user is redirected to the home page
    """
    login(page, "robottiTeacher", "eat")
    expect(page).to_have_title(re.compile("Jakaja"))


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


def test_go_to_all_surveys_page(setup_db, page: Page):
    """
    Test that the user can go to the all surveys page from the front page
    """
    login(page, "robottiTeacher", "train")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    expect(page.get_by_text("Kyselyn tila")).to_be_visible()
    expect(page.get_by_text("Toiminnot")).to_be_visible()


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


def test_survey_more_info_works(setup_db, page: Page, create_survey_with_csv_file):
    """
    Test that if a survey choice has additional info, it is displayed when clicked and hidden when clicked again
    """
    login(page, "robottiTeacher", "repeat")
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
    login(page, "robottiTeacher", "eat")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Päiväkoti valinta").click()
    expect(page.get_by_text("Päiväkoti valinta").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Toivo").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Floora").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Kotikallio").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Nalli").first).to_be_visible()
    page.get_by_test_id("submit-button").click()
    #expect(page.get_by_text("Tallennus epäonnistui. Valitse vähintään 4")).to_be_visible()
    page.get_by_text("Päiväkoti Toivo").drag_to(page.locator("[data-rfd-droppable-id='good']"))

    
    
    
    


    #page.wait_for_timeout(500)
    page.get_by_text("Päiväkoti Floora").drag_to(page.locator("[data-rfd-droppable-id='good']"))
    #page.wait_for_timeout(500)
    page.get_by_text("Päiväkoti Kotikallio").drag_to(page.locator("[data-rfd-droppable-id='good']"))
    #page.wait_for_timeout(500)
    page.get_by_text("Päiväkoti Nalli").drag_to(page.locator("[data-rfd-droppable-id='good']"))
    #page.wait_for_timeout(500)
    page.get_by_test_id("submit-button").click()
    expect(page.get_by_text("Tallennus onnistui.")).to_be_visible()


def test_delete_survey_answer(setup_db, page: Page, create_survey_with_csv_file):
    """
    Test that a user can delete their submitted ranking
    """

    # First we answer survey
    login(page, "robottiTeacher", "eat")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Päiväkoti valinta").click()
    expect(page.get_by_text("Päiväkoti valinta").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Toivo").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Floora").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Kotikallio").first).to_be_visible()
    expect(page.get_by_text("Päiväkoti Nalli").first).to_be_visible()
    page.locator("#submitDoesntExistButton").click()
    expect(page.get_by_text("Tallennus epäonnistui. Valitse vähintään 4")).to_be_visible()
    expect(page.get_by_text("Tallennus epäonnistui. Valitse vähintään 4")).to_be_hidden()
    page.get_by_text("Päiväkoti Toivo").drag_to(page.locator("xpath=//*[@id='sortable-good']"))
    page.wait_for_timeout(500)
    page.get_by_text("Päiväkoti Floora").drag_to(page.locator("xpath=//*[@id='sortable-good']"))
    page.wait_for_timeout(500)
    page.get_by_text("Päiväkoti Kotikallio").drag_to(page.locator("xpath=//*[@id='sortable-good']"))
    page.wait_for_timeout(500)
    page.get_by_text("Päiväkoti Nalli").drag_to(page.locator("xpath=//*[@id='sortable-good']"))
    page.wait_for_timeout(500)
    page.locator("#submitDoesntExistButton").click()
    expect(page.get_by_text("Tallennus onnistui.")).to_be_visible()

    page.locator("#dropdownMenuButton1").click()
    page.get_by_text("Kirjaudu ulos").click()

    # Delete answers
    login(page, "robottiTeacher", "sleep")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Päiväkoti valinta").click()
    page.locator("#deleteSubmission").click()
    expect(page.get_by_text("Oletko varma?")).to_be_visible()
    page.locator("#confirmDelete").click()
    expect(page.get_by_text("Valinnat poistettu")).to_be_visible()


def test_logging_out(setup_db, page: Page):
    """
    Test that logging user out works
    """
    login(page, "robottiTeacher", "skong")
    page.locator("#dropdownMenuButton1").click()
    page.get_by_text("Kirjaudu ulos").click()
    expect(page.get_by_text("Käyttäjätunnus")).to_be_visible()
    expect(page.get_by_text("Salasana")).to_be_visible()


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
