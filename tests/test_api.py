"""API behaviour tests.

ONE example is written for you. Replace each `assert False` TODO with a real test.
Use the helpers from conftest:  login(client, user, pw) -> token,  auth(token) -> header.
Ask for the `client` fixture by adding it as a parameter (it gives you a fresh DB each time).

Run the suite:   pytest -q
Run one file:    pytest tests/test_api.py -q
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


# ----- TODO 1 -------------------------------------------------------------
def test_register_then_login(client):
    # Register a new user, then log in as that user.
    # Assert login returns 200 AND the access_token looks like a JWT
    # (three dot-separated parts: token.count(".") == 2).
    # Arrange: register a brand-new user
    reg = client.post("/register", json={"username": "carol", "password": "carolpass"})
    assert reg.status_code == 200

    # Act: log in as that user
    res = client.post("/login", json={"username": "carol", "password": "carolpass"})

    # Assert: 200 and the token has 3 dot-separated parts (header.payload.signature)
    assert res.status_code == 200
    assert res.json()["access_token"].count(".") == 2


# ----- TODO 2 -------------------------------------------------------------
def test_login_wrong_password_is_401(client):
    # Log in as 'alice' with the WRONG password. Assert the status code is 401.
    # Act: alice exists, but the password is wrong
    res = client.post("/login", json={"username": "alice", "password": "not-her-password"})

    # Assert: refused with 401
    assert res.status_code == 401


# ----- TODO 3 -------------------------------------------------------------
def test_create_then_list_own_note(client):
    # Log in as alice, POST a new note, then GET /notes and assert the new
    # note's title appears in the list.
    # Arrange: log in as alice
    token = login(client, "alice", "alicepass")

    # Act: create a note, then list alice's notes
    created = client.post(
        "/notes",
        json={"title": "My new note", "body": "Written during the test"},
        headers=auth(token),
    )
    res = client.get("/notes", headers=auth(token))

    # Assert: creation worked and the new title is in her list
    assert created.status_code == 200
    assert res.status_code == 200
    titles = [note["title"] for note in res.json()]
    assert "My new note" in titles
