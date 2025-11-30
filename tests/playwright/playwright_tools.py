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

    page.locator(".right-column").scroll_into_view_if_needed()
    page.wait_for_timeout(50)

    s.scroll_into_view_if_needed()
    t.scroll_into_view_if_needed()

    s.wait_for()
    t.wait_for()

    sbox = s.bounding_box()
    tbox = t.bounding_box()

    page.wait_for_timeout(0)
    sbox = s.bounding_box()

    sx = sbox["x"] + sbox["width"] / 2
    sy = sbox["y"] + sbox["height"] / 2
    tx = tbox["x"] + tbox["width"] / 2
    ty = tbox["y"] + tbox["height"] / 2

    # Move to source
    page.mouse.move(sx, sy)
    page.mouse.down()

    # Activate drag sensor
    page.mouse.move(sx, sy + 10, steps=5)

    page.mouse.move(tx, ty, steps=20)

    page.mouse.up()

    page.wait_for_timeout(50)
