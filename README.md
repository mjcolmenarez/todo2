Minimal Django to-do with:
- List + create/edit/delete + toggle
- Kanban (todo/doing/done)
- CSV export of tasks

## Dev setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

## Features
- Sort by due date / priority / newest
- Filter by status (All/To-do/Doing/Done)
- Quick-add from the list page
- CSV export respects sorting/filter
