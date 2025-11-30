import os
from playwright.sync_api import Page, expect
from .playwright_tools import login


def test_login(setup_db, page: Page):
    """
    Test that mock login works. After login the user is redirected to the home page
    """
    username = "robottiTeacher"
    password = "skong"

    base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000/")
    page.goto(base_url)
    page.get_by_test_id("username").fill(username)
    page.get_by_test_id("password").fill(password)
    page.get_by_test_id("login-button").click()

    expect(page.get_by_text("Näytä vanhat kyselyt")).to_be_visible()
    expect(page.get_by_text("Käyttäjätunnus")).to_be_hidden()
    expect(page.get_by_text("Salasana")).to_be_hidden()


def test_login_with_wrong_username(setup_db, page: Page):
    """
    Test that logging in with a wrong username fails
    """
    username = "roboTeach"
    password = "skong"

    base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000/")
    page.goto(base_url)
    page.get_by_test_id("username").fill(username)
    page.get_by_test_id("password").fill(password)
    page.get_by_test_id("login-button").click()

    expect(page.get_by_text("Kirjautuminen epäonnistui")).to_be_visible()
    expect(page.get_by_text("Käyttäjätunnus")).to_be_visible()
    expect(page.get_by_text("Salasana")).to_be_visible()


def test_logging_out(setup_db, page: Page):
    """
    Test that logging user out works.
    """
    login(page, "robottiTeacher", "skong")
    page.locator("#dropdownMenuButton1").click()
    page.get_by_text("Kirjaudu ulos").click()
    expect(page.get_by_text("Käyttäjätunnus")).to_be_visible()
    expect(page.get_by_text("Salasana")).to_be_visible()
