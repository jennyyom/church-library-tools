# Church Library Tools

Small tools that help volunteers run a church library.

> **Status: In progress.** The overdue-reminder logic works and is tested against
> made-up sample data. It is **not yet connected** to the library's real data.
> The volunteer dashboard is planned.

## Why This Project

The library runs on **Handy Library**, a purchased Windows program backed by a
Firebird database. We cannot change its code, and volunteers have run into a few
problems with it:

- **Overdue reminder emails show garbled Korean text** for recipients.
- **Reminder emails currently fail to send.** Gmail rejects the program's login
  (`535 5.7.8 Username and Password not accepted`), because Gmail no longer
  accepts a regular account password from third-party programs.
- **Loan information is hard to find.** Volunteers struggle to answer simple
  questions like "who has this book?" or "which books are popular?"

These tools work **alongside** Handy Library. They **only read** its data and never
change the program or its database.

## Features

| Feature | Status |
|---|---|
| Overdue reminders: find overdue loans, one email per person | Logic done and tested on sample data |
| Read loans directly from the Firebird database (read-only) | Planned. Practicing on a copy of the database |
| Volunteer dashboard | Planned |
| Borrow count per book, most borrowed books this month | Planned (shown on the dashboard) |
| New-book alert: email the member who requested a book when it is purchased | Planned |

### Overdue book reminders

1. **Read** loan records (`notifier/loans.py`)
2. **Find overdue loans**: not returned, and the due date is before today
3. **Group by person** so someone with three late books gets one email (`notifier/messages.py`)
4. **Skip people reminded in the last 7 days** using a small local log (`notifier/sent_log.py`)
5. **Preview or send** the emails (`notifier/mailer.py`)
6. **List members with no email** so a librarian can contact them directly

Emails are built with Python's `EmailMessage`, which encodes Korean text as UTF-8.

`notifier/loans.py` is the only file that knows where the data comes from. It
currently reads a CSV file. Switching to the database means adding one reader
function there; the rest of the code and its tests stay the same.

### Volunteer dashboard (planned)

A simple local web page for volunteers, built with Streamlit:

- Overdue loans, with an email preview and a confirm step before anything is sent
- How many times each book has been borrowed
- Most borrowed books this month
- Members with no email on file, for direct contact

Handy Library already shows some of this (for example, per-book borrow counts in
its Circulation view), but volunteers did not know where to find it. The goal is
to put what they need on one screen.

## How the Tools Reach the Library Data

The library computer is on the church's private network. During development:

- I connect from my Mac through the church's **WireGuard VPN**, using a client
  configuration issued to me by the church IT team.
- I use **Windows Remote Desktop** to work on the library computer.
- I develop and test against a **copy** of the library database, not the live one.

Connection details (VPN configuration, IP addresses, accounts) are not stored in
this repository. See [Security and Privacy](#security-and-privacy).

### Before switching to real data

- [ ] Check how Handy Library runs Firebird. In server mode, we can read while the
  program is open. In embedded mode, the program may lock the database file.
- [ ] Get a **read-only** database account from the church IT team.
- [ ] Add a database reader in `notifier/loans.py`. Keep connection settings in
  environment variables, not in the code.
- [ ] In `dashboard.py`, change `LOANS_PATH` (or the reader it uses) to the real data.
- [ ] Make sure real data files stay in `data/` so `.gitignore` keeps them out of Git.

## Run It

```bash
pip install -r requirements.txt

# Preview only (default). Nothing is sent.
python main.py data/sample_loans.csv --today 2026-10-04

# Send for real (needs email settings below)
python main.py path/to/loans.csv --send
```

### Email settings (only needed with `--send`)

Set these as environment variables. Never put the password in the code.

| Variable | Example |
|---|---|
| `SMTP_USER` | library@example.com |
| `SMTP_PASSWORD` | Gmail App Password (requires 2-Step Verification) |
| `SMTP_HOST` | smtp.gmail.com (default) |
| `SMTP_PORT` | 587 (default) |

## Tests

```bash
python -m pytest -v
```

The tests cover the edge cases that matter most:

- A book due **today** is not overdue yet
- Returned books are never reminded
- Two books for the same person (even with different email capitalization) become **one** email
- Family members who **share one email address** each get their own reminder
- Members **without an email** go to a manual contact list instead
- Nobody is reminded twice within 7 days, even after the program restarts
- A row with a bad date is reported and skipped instead of crashing the run

## Security and Privacy

This project handles church members' personal information, so:

- **Never committed:** VPN configuration files and keys, server and computer IP
  addresses, database files, passwords, real member names and emails, and the send log.
  These are listed in `.gitignore`.
- **Passwords** are read from environment variables only.
- `data/sample_loans.csv` contains **made-up names only**.
- The dashboard will run **only on the library computer**, so member data does not
  leave the church network.

## Roadmap

- [x] Find overdue loans and build one email per person
- [x] Dry-run preview by default
- [x] Duplicate-send protection
- [ ] Document the database structure (tables and columns only, no member data)
- [ ] Read loans directly from the database, read-only
- [ ] Borrow count per book and most borrowed books this month
- [ ] Volunteer dashboard (Streamlit)
- [ ] Email the requester when a requested book is purchased
- [ ] Install on the library computer and collect volunteer feedback
- [ ] (Optional) Text message reminders for members who opt in
