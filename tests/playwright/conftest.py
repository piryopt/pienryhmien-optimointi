import pytest
from pathlib import Path
from playwright.sync_api import Page, expect
from .playwright_tools import login

TEST_FILES_PATH = Path(__file__).parent / ".." / "test_files"


@pytest.fixture(scope="function", autouse=True)
def trace_on_failure(context, request):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    if request.node.rep_call.failed:
        trace_path = f"trace_{request.node.name}.zip"
        context.tracing.stop(path=trace_path)
    else:
        context.tracing.stop()


@pytest.fixture
def create_survey_with_csv_file(page: Page):
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

    page.locator("#dropdownMenuButton1").click()
    page.get_by_text("Kirjaudu ulos").click()
