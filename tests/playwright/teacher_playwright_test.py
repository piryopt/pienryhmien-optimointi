import re
from playwright.sync_api import Page, expect
from playwright_tools import login

def test_login_as_teacher(page: Page):
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
    page.get_by_role("link", name="Luo uusi kysely Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta").click()
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
    page.goto("http://127.0.0.1:5000/surveys/create")
