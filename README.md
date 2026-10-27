# Church Library Tools

Small tools that help volunteers run a church library.

The library runs on an older Windows program backed by a Firebird database.
These tools **do not change that program or its data**. They only read loan
and book records and act on them.

> **Status: In progress.** Overdue reminders work. The other features are being built.

## Features

| Feature | Status |
|---|---|
| Overdue book email reminders | Working. Fixing Korean text that appears garbled in emails |
| Borrow count per book | Planned |
| New-book alert: email the member who requested a book when it is purchased | Planned |

### Overdue book reminders

1. **Read** loan records (`notifier/loans.py`)
2. **Find overdue loans**: not returned, and the due date is before today
3. **Group by person** so someone with three late books gets one email (`notifier/messages.py`)
4. **Skip people reminded in the last 7 days** using a small local log (`notifier/sent_log.py`)
5. **Preview or send** the emails (`notifier/mailer.py`)
6. **List members with no email** so a librarian can contact them directly

## How the Tools Reach the Library Data

The library computer is on the church's private network. During development:

- I connect from my Mac through the church's **WireGuard VPN**, using a client
  configuration issued to me by the church IT team.
- I use **Windows Remote Desktop** to work on the library computer.
- I develop and test against a **copy** of the library database, not the live one.

Connection details (VPN configuration, IP addresses, accounts) are not stored in
this repository. See [Security and Privacy](#security-and-privacy).

## Run It

```bash
pip install -r requirements.txt

# Preview only (default). Nothing is sent.
python main.py data/sample_loans.csv --today 2026-10-04

# Send for real (needs email settings below)
python main.py path/to/export.csv --send
```

### Email settings (only needed with `--send`)

Set these as environment variables. Never put the password in the code.

| Variable | Example |
|---|---|
| `SMTP_USER` | library@yourchurch.org |
| `SMTP_PASSWORD` | Gmail App Password |
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

## Known Issues

- **Korean text is garbled in sent reminder emails.** Investigating where the text
  breaks: when reading from the database, or when building the email.

## Security and Privacy

This project handles church members' personal information, so:

- **Never committed:** VPN configuration files and keys, server and computer IP
  addresses, database files, passwords, real member names and emails, and the send log.
  These are listed in `.gitignore`.
- **Passwords** are read from environment variables only.
- `data/sample_loans.csv` contains **made-up names only**.

## Roadmap

- [x] Find overdue loans and build one email per person
- [x] Dry-run preview by default
- [x] Duplicate-send protection
- [ ] Fix garbled Korean text in reminder emails
- [ ] Read the library database directly (currently testing on a copy)
- [ ] Show how many times each book has been borrowed
- [ ] Email the requester when a requested book is purchased
- [ ] Run weekly with Windows Task Scheduler
- [ ] (Optional) Text message reminders for members who opt in
