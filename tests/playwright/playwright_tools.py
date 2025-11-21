import os


def login(page, username, password):
    """
    Helper function for logging the user in
    """
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000/")
    page.goto(base_url)
    page.get_by_test_id("username").fill(username)
    page.get_by_test_id("password").fill(password)
    page.get_by_test_id("login-button").click()


def mouse_dnd(page, source: str, target: str):
    """
    Helper function for dragging and dropping for survey answer page
    args:
        source: text on the draggable item
        target: dnd id of the drop area
    """
    # Items located by text, answer boxes located by dnd id

    s = page.get_by_text(source)
    t = page.locator(target)

    s.scroll_into_view_if_needed()
    t.scroll_into_view_if_needed()

    s = s.bounding_box()
    t = t.bounding_box()

    # Hold mouse on location
    page.mouse.move(s["x"] + s["width"] / 2, s["y"] + s["height"] / 2)
    page.mouse.down()

    # Move to target location
    page.mouse.move(s["x"] + s["width"] / 2, s["y"] + s["height"] / 2)
    page.mouse.move(t["x"] + t["width"] / 2, t["y"] + t["height"] / 2, steps=15)

    # Release
    page.mouse.up()
