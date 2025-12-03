def test_login_page_loads(client):
    """
    The login page should return HTTP 200.
    """
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data  # checks that 'Login' text is on the page


def test_protected_route_redirects_when_not_logged_in(client):
    """
    Access to a protected page (e.g., dashboard) should redirect
    to the login page if the user is not authenticated.
    """
    response = client.get("/dashboard", follow_redirects=False)
    # Flask-Login uses 302 redirect to login page
    assert response.status_code in (301, 302)
    # Location header should point to login route
    assert "/login" in (response.headers.get("Location") or "")
