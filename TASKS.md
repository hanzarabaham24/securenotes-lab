# Combined Lab — Checklist

## Part A — make the security real (`app/main.py`)
- [x] **TASK 1 (A04)** hash_password / verify_password use bcrypt
- [x] **TASK 2 (A07)** create_token / read_token use a signed, expiring JWT
- [x] **TASK 3 (A07)** get_current_user raises 401 on a bad/expired token or unknown user (fail closed)
- [x] **TASK 4 (A01)** get_note returns 403 when the note isn't the caller's
- [x] **TASK 5 (A01)** /admin/users requires the admin role and never returns the password column

## Part B — write the tests (`tests/`)
API (`test_api.py`)
- [x] register then login returns a JWT (three dotted parts)
- [x] wrong password returns 401
- [x] create a note, then see it in your list

Security (`test_security.py`)
- [x] bad token rejected (401)
- [x] a user can't read another's note (403)  ← A01
- [x] a user can read their own note (200)
- [x] same login error for bad user vs bad password  ← A07
- [x] a non-admin can't list users (403)  ← A01
- [x] admin list has no password field  ← A04

**Goal:** all 5 tasks done AND all 11 tests green (`pytest -q`). Then `pytest --cov=app`.

## Reflection (4–5 sentences)
Pick one security test. Explain what it checks, which OWASP risk it guards, and what would break in the
app if a teammate deleted that one check.

I picked `test_user_cannot_read_another_users_note`. It logs in as Alice, requests note 2 (which belongs to Bob), and asserts that the server answers 403. It guards against OWASP A01, Broken Access Control, specifically IDOR, where a logged-in user changes the ID in the URL to read someone else's data. If a teammate deleted the ownership check in `get_note`, any logged-in user could read every note just by trying IDs like 1, 2 and 3, and this test would be the only thing that failed. That is why it is valuable: it catches the mistake automatically before the code reaches users.