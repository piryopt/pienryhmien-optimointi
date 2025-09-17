from pathlib import Path
import re
from playwright.sync_api import Page, expect
from playwright_tools import login

FILE_TO_UPLOAD = Path(__file__).parent / ".." / "test_files" / "test_survey1.csv"


def test_login(page: Page):
    """
    Test that mock ad login works. After login the user is redirected to the home page
    """
    login(page, "robottiTeacher", "eat")
    expect(page).to_have_title(re.compile("Etusivu - Jakaja"))


def test_go_to_create_survey_page(page: Page):
    """
    Test that the user can go to the create new survey page from the front page
    """
    login(page, "robottiTeacher", "sleep")
    page.get_by_role(
        "link",
        name="Luo uusi kysely Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta",
    ).click()
    expect(page).to_have_title(re.compile("Luo uusi kysely - Jakaja"))


def test_go_to_all_surveys_page(page: Page):
    """
    Test that the user can go to the all surveys page from the front page
    """
    login(page, "robottiTeacher", "train")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    expect(page).to_have_title(re.compile("Aiemmat kyselyt - Jakaja"))


def test_create_new_survey(page: Page):
    """
    Test that the user is able to create a new survey
    """
    login(page, "robottiTeacher", "abuse gear")
    page.get_by_role(
        "link",
        name="Luo uusi kysely Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta",
    ).click()
    page.locator("#groupname").fill("Menaces")
    page.locator("#end-date").fill("31.12.2028")
    page.locator("#endtime").select_option("23:00")
    page.locator("#survey-information").fill("Absolute menaces to society")
    page.locator("xpath=//*[@id='choiceTable']/tr/td[2]").click()
    page.keyboard.type("Vegeta")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("5")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("0")
    page.locator("xpath=//*[@id='add-column-header']").click()
    page.keyboard.type("Quotes")
    page.keyboard.press("Enter")
    page.locator("xpath=//*[@id='choiceTable']/tr/td[5]").click()
    page.keyboard.type("Trespass into the domain of the Gods!")
    page.locator("#add_choice").click()
    page.locator("xpath=//*[@id='choiceTable']/tr[2]/td[2]").click()
    page.keyboard.type("Barou")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("5")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("0")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("Talent without hard work is nothing.")
    page.locator("#add_choice").click()
    page.locator("xpath=//*[@id='choiceTable']/tr[3]/td[2]").click()
    page.keyboard.type("Isagi")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("5")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("0")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.keyboard.type("How does it feel to be the clown of my story?")
    page.keyboard.press("Enter")
    page.wait_for_timeout(500)
    page.locator("#create_survey").click()
    # page.screenshot(path="playwright-report/afterclick.png", full_page=True)
    expect(page.get_by_text("Uusi kysely luotu!")).to_be_visible()


def test_create_new_survey_with_csv_file(page: Page):
    """
    Test that the user is able to create a new survey with a pre-made CSV file
    """
    login(page, "robottiTeacher", "RoboCop")
    page.get_by_role(
        "link",
        name="Luo uusi kysely Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta",
    ).click()
    page.locator("#groupname").fill("Päiväkoti valinta")
    page.locator("#end-date").fill("31.08.2029")
    page.locator("#endtime").select_option("12:00")
    page.locator("#survey-information").fill(
        "Valitse mihin päiväkotiin haluat sijoittaa itsesi"
    )

    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Tuo valinnat CSV-tiedostosta").click()
    file_chooser = fc_info.value
    file_chooser.set_files(str(FILE_TO_UPLOAD))
    expect(page.get_by_text("Päiväkoti Toivo")).to_be_visible()
    expect(page.get_by_text("Tässä tekstiä,, kahdella pilkulla")).to_be_visible()
    page.locator("#create_survey").click()
    expect(page.get_by_text("Uusi kysely luotu!")).to_be_visible()


def test_survey_more_info_works(page: Page):
    """
    Test that if a survey choice has additional info, it is displayed when clicked and hidden when clicked again
    """
    login(page, "robottiTeacher", "repeat")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Menaces").click()
    page.get_by_text("Isagi").click()
    expect(
        page.get_by_text("Quotes: How does it feel to be the clown of my story?").first
    ).to_be_visible()
    page.get_by_text("Isagi").click()
    expect(
        page.get_by_text("Quotes: How does it feel to be the clown of my story?").first
    ).to_be_hidden()


def test_answer_survey(page: Page):
    """
    Test that a user can answer a created survey
    """
    login(page, "robottiTeacher", "eat")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Menaces").click()
    expect(page.get_by_text("Menaces").first).to_be_visible()
    expect(page.get_by_text("Vegeta").first).to_be_visible()
    expect(page.get_by_text("Barou").first).to_be_visible()
    expect(page.get_by_text("Isagi").first).to_be_visible()
    page.locator("#submitDoesntExistButton").click()
    expect(
        page.get_by_text("Tallennus epäonnistui. Valitse vähintään 3")
    ).to_be_visible()
    expect(
        page.get_by_text("Tallennus epäonnistui. Valitse vähintään 3")
    ).to_be_hidden()
    page.get_by_text("Barou").drag_to(page.locator("xpath=//*[@id='sortable-good']"))
    page.wait_for_timeout(500)
    page.get_by_text("Isagi").drag_to(page.locator("xpath=//*[@id='sortable-good']"))
    page.wait_for_timeout(500)
    page.get_by_text("Vegeta").drag_to(page.locator("xpath=//*[@id='sortable-good']"))
    page.wait_for_timeout(500)
    page.locator("#submitDoesntExistButton").click()
    expect(page.get_by_text("Tallennus onnistui.")).to_be_visible()


def test_delete_survey_answer(page: Page):
    """
    Test that a user can delete their submitted ranking
    """
    login(page, "robottiTeacher", "sleep")
    page.get_by_role("link", name="Näytä vanhat kyselyt").click()
    page.get_by_role("link", name="Menaces").click()
    page.locator("#deleteSubmission").click()
    expect(page.get_by_text("Oletko varma?")).to_be_visible()
    page.locator("#confirmDelete").click()
    expect(page.get_by_text("Valinnat poistettu")).to_be_visible()


def test_logging_out(page: Page):
    """
    Test that logging user out works
    """
    login(page, "robottiTeacher", "skong")
    page.locator("#dropdownMenuButton1").click()
    page.get_by_text("Kirjaudu ulos").click()
    expect(page.get_by_text("Salasana (laita mitä vaan)")).to_be_visible()
