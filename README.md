# todo2 — To-Do App

A compact, modern to-do app built with Django and SQLite. It focuses on a clean UI and two views for working with tasks:

- **List view** with create/edit/delete and a one-click **toggle** to mark tasks done.
- **Kanban board** (Todo / Doing / Done) for quick drag-style status changes.
- **CSV export** that respects the current sort/filter.

---

## Quick start

**Requirements:** Python 3.10+ (tested with 3.13), pip, virtualenv (optional).

```bash
git clone <your-repo-url>
cd todo2

# Create & activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database and run
python manage.py migrate
python manage.py runserver

Open http://127.0.0.1:8000/
 in your browser.