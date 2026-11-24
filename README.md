# Library Management System

A complete Library Management System built with **Django + MySQL** for a
college project. It includes book management, member management, issuing
and returning books, automatic overdue detection, search, and a secure
admin login.

This project has been fully built, tested end-to-end against a real MySQL
database, and verified to run without errors before being packaged for you.

---

## 1. What's inside this ZIP

```
library_management_system/
├── manage.py                   Django's command-line tool
├── requirements.txt             Python packages needed
├── README.md                    This file
├── .env.example                 Template for your MySQL password (copy this)
├── .gitignore
├── setup.bat                    Double-click to set everything up (Windows)
├── run.bat                      Double-click to start the website (Windows)
│
├── database/
│   └── library_management.sql   Full database + 10 sample books, 5 members
│
├── library_project/             Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── library/                     The main app (models, views, templates)
    ├── models.py                 Book, Member, IssueRecord
    ├── views.py
    ├── forms.py
    ├── admin.py
    ├── urls.py
    ├── migrations/                Already generated for you
    ├── templates/                 All HTML pages (Bootstrap styled)
    └── static/css/style.css
```

You do **not** need to create any files yourself. Everything is ready.

---

## 2. What you need installed on your computer first

* **Python 3.10+** — https://www.python.org/downloads/ (when installing, tick
  "Add Python to PATH")
* **MySQL Server** (MySQL Community Server or XAMPP/WAMP with MySQL) —
  https://dev.mysql.com/downloads/installer/
* **MySQL Workbench** (optional but recommended, to see your data visually)
* **VS Code**

---

## 3. Step-by-step setup (Windows)

### Step 1 — Extract the ZIP
Extract it anywhere, e.g. `C:\Projects\library_management_system`, then open
that folder in VS Code.

### Step 2 — Open a terminal in VS Code
`Terminal` → `New Terminal` (make sure it opens **inside** the project
folder).

### Step 3 — Create the database in MySQL

Open **MySQL Workbench**, connect to your local MySQL server, then:

1. Go to **File → Open SQL Script...**
2. Select `database/library_management.sql` from this project
3. Click the ⚡ **lightning bolt (Execute)** button to run the whole script

This automatically creates the `library_management` database, all the
tables, and loads **10 sample books, 5 sample members, and 6 sample issue
records** so the site isn't empty when you first open it.

*(Command-line alternative, if you don't use Workbench):*
```
mysql -u root -p < database/library_management.sql
```

### Step 4 — Enter your MySQL password (the ONE place you need to edit)

In the project folder, find the file **`.env.example`**.

1. Make a copy of it
2. Rename the copy to exactly **`.env`**
3. Open `.env` in VS Code — it looks like this:

```
DB_NAME=library_management
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD   <-- put your real MySQL password here
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=YOUR_DJANGO_SECRET_KEY
```

4. Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL root password
   (if your MySQL root user has no password, just leave it as
   `DB_PASSWORD=`)
5. Save the file

This `.env` file is the **only place** your password needs to be typed. It
is never uploaded or hard-coded anywhere else, and `.gitignore` already
excludes it if you use Git.

### Step 5 — Run the automatic setup script

Double-click **`setup.bat`** in the project folder (or run it from the
terminal: `setup.bat`). It will:

* Create a virtual environment (`venv`)
* Install Django, PyMySQL and python-dotenv
* Apply Django's internal migrations (auth, sessions, admin, etc.)

*(If you prefer typing commands manually instead of setup.bat, see
Section 5 below.)*

### Step 6 — Create your admin login

In the same terminal (with `venv` active — you'll see `(venv)` at the start
of the line):

```
python manage.py createsuperuser
```

It will ask for a username, email (optional — you can leave it blank) and
password. Remember what you type — this is how you log in to the website
and to `/admin/`.

### Step 7 — Start the website

Double-click **`run.bat`**, or run:

```
python manage.py runserver
```

### Step 8 — Open it in Chrome

Go to:

```
http://127.0.0.1:8000/
```

Log in with the superuser account you just created. You'll land on the
Dashboard, already showing the 10 sample books and 5 sample members from
the SQL file.

The Django admin panel (extra, optional, powerful management view) is at:

```
http://127.0.0.1:8000/admin/
```

---

## 4. Login credentials

There is **no pre-made username/password** baked into the database for
security reasons — you create your own in Step 6 above
(`python manage.py createsuperuser`). This is the account you use both for
the website and for `/admin/`.

---

## 5. Manual setup commands (if you don't want to use setup.bat)

```
cd library_management_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

REM (create your .env file first — see Step 4 above)
REM (import database/library_management.sql in MySQL Workbench — see Step 3)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in Chrome.

---

## 6. Features included

* **Dashboard** — total books, members, issued books, available copies,
  overdue count, recent issues/returns
* **Book Management** — add, view, search (title/author/ISBN/category),
  edit, delete, view details, with validation
* **Member Management** — add, view, search (name/email/phone), edit,
  delete, view details
* **Issue Book** — pick member + book + dates; blocks issuing when no
  copies are available; automatically reduces available quantity
* **Return Book** — one click; automatically restores available quantity
  and marks the record as Returned
* **Overdue Books** — automatically calculated from today's date vs. due
  date, shown with the number of overdue days
* **Search** — available on Books, Members, Issued Books, Returned Books
  and Overdue Books pages
* **Admin Login** — Django's built-in authentication; all management pages
  require login
* **Django Admin** — all three models registered with useful list views,
  filters and search
* **Responsive Bootstrap UI** — sidebar navigation, cards, tables, alerts

---

## 7. Troubleshooting

**"Access denied for user 'root'@'localhost'"**
→ Your password in `.env` doesn't match your real MySQL password. Double
check it and save the file again.

**"Unknown database 'library_management'"**
→ You haven't run the SQL file yet — go back to Step 3.

**"No module named 'django'" / "'python' is not recognized"**
→ Make sure your virtual environment is active — you should see `(venv)`
at the start of your terminal line. If not, run `venv\Scripts\activate`
again, or reinstall Python with "Add Python to PATH" checked.

**Page looks unstyled (no colors/cards)**
→ Bootstrap loads from the internet (via CDN), so make sure you have an
internet connection when viewing the site.

---

## 8. Notes on how it was verified

Before packaging, this project was actually installed with Django, PyMySQL
and python-dotenv, a real local MySQL server was created, the SQL file was
imported, and every page — dashboard, books, members, issue, return,
overdue, search, admin, add/edit/delete — was tested end-to-end (login,
form submissions, quantity updates, and overdue detection all confirmed
working) before this ZIP was created for you.
