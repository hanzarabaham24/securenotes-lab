"""Security tests — the most valuable tests you'll write this week.

Each one locks in an OWASP rule from Weeks 13-14 so a future change can't quietly
reopen the hole. ONE example is done; replace each `assert False` TODO with a real test.

Seed data reminder:  note 1 belongs to ALICE, note 2 belongs to BOB.
Accounts:  admin/admin123 (admin) · alice/alicepass · bob/bobpass
"""
from tests.conftest import login, auth


# ----- EXAMPLE (already done) ---------------------------------------------
def test_protected_route_rejects_no_token(client):
    res = client.get("/notes")               # no Authorization header
    assert res.status_code == 401            # A07: auth is required


# ----- TODO 1 -------------------------------------------------------------
def test_protected_route_rejects_bad_token(client):
    # Call GET /notes with a junk token, e.g. auth("not.a.jwt").
    # Assert 401 — the app must fail closed on an invalid token.
    res = client.get("/notes", headers=auth("not.a.jwt"))   # Act: junk token
    assert res.status_code == 401                            # Assert: A07 fail closed


# ----- TODO 2  (A01 — the big one) ----------------------------------------
def test_user_cannot_read_another_users_note(client):
    # Log in as alice. Try GET /notes/2 (that note belongs to Bob).
    # Assert 403 — ownership must be enforced.
    alice = login(client, "alice", "alicepass")              # Arrange
    res = client.get("/notes/2", headers=auth(alice))        # Act (note 2 is Bob's)
    assert res.status_code == 403                            # Assert — A01


# ----- TODO 3 -------------------------------------------------------------
def test_user_can_read_own_note(client):
    # Log in as alice. GET /notes/1 (hers). Assert 200.
    alice = login(client, "alice", "alicepass")              # Arrange
    res = client.get("/notes/1", headers=auth(alice))        # Act (note 1 is Alice's)
    assert res.status_code == 200                            # Assert
    assert res.json()["title"] == "Alice diary"


# ----- TODO 4  (A07 — no user enumeration) --------------------------------
def test_login_does_not_reveal_which_field_was_wrong(client):
    # POST /login once with a username that doesn't exist, once with a real
    # username but wrong password. Assert the two error bodies are IDENTICAL.
    # Act: one attempt with an unknown user, one with a real user + wrong password
    bad_user = client.post("/login", json={"username": "ghost", "password": "whatever"})
    bad_pass = client.post("/login", json={"username": "alice", "password": "wrong"})

    # Assert: both are 401 and the error bodies are identical (A07: no user enumeration)
    assert bad_user.status_code == 401
    assert bad_pass.status_code == 401
    assert bad_user.json() == bad_pass.json()


# ----- TODO 5  (A01 — role) -----------------------------------------------
def test_non_admin_cannot_list_users(client):
    # Log in as alice (not an admin). GET /admin/users. Assert 403.
    alice = login(client, "alice", "alicepass")              # Arrange: a normal user
    res = client.get("/admin/users", headers=auth(alice))    # Act
    assert res.status_code == 403                            # Assert — A01 role check


# ----- TODO 6  (A04 — no hash leak) ---------------------------------------
def test_admin_can_list_users_without_password_leak(client):
    # Log in as admin. GET /admin/users. Assert 200 AND no item in the
    # response contains a "password" field.
    admin = login(client, "admin", "admin123")               # Arrange
    res = client.get("/admin/users", headers=auth(admin))    # Act

    assert res.status_code == 200                            # Assert: admin is allowed
    users = res.json()
    assert len(users) > 0                                    # the list is not empty
    for user in users:
        assert "password" not in user                        # A04: no hash leak
