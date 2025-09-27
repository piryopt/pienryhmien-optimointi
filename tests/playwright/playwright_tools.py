import os
import pytest


# Add to imports of survey_testing.py to get more info
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": "videos/",
        "record_har_path": "network.har",
    }


@pytest.fixture(scope="function", autouse=True)
def trace_on_failure(context, request):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    if request.node.rep_call.failed:
        trace_path = f"trace_{request.node.name}.zip"
        context.tracing.stop(path=trace_path)
    else:
        context.tracing.stop()



def login(page, username, password):
    """
    Helper function for logging the user in
    """
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000/")
    page.goto(base_url)
    page.locator("#nameid").fill(username)
    page.get_by_label("Salasana (laita mitä vaan):").fill(password)
    page.get_by_role("button").click()
