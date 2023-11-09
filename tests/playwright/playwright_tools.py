def login(page, username, password):
    """
    Helper function for logging the user in
    """
    page.goto("http://127.0.0.1:5000/")
    page.locator("#nameid").fill(username)
    page.get_by_label("Salasana (laita mitä vaan):").fill(password)
    page.get_by_role("button").click()