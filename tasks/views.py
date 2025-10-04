from datetime import date, timedelta
import calendar

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Task


# ---------- Basic CRUD ----------

class TaskList(ListView):
    template_name = "tasks/list.html"
    model = Task
    context_object_name = "tasks"

    def get_queryset(self):
        return (
            Task.objects.all()
            .order_by("due_date", "-priority", "title")
        )


class TaskCreate(CreateView):
    model = Task
    template_name = "tasks/form.html"
    fields = ["title", "description", "due_date", "priority", "status"]
    success_url = reverse_lazy("tasks:list")


class TaskUpdate(UpdateView):
    model = Task
    template_name = "tasks/form.html"
    fields = ["title", "description", "due_date", "priority", "status"]
    success_url = reverse_lazy("tasks:list")


class TaskDelete(DeleteView):
    model = Task
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:list")


# ---------- Kanban ----------

def kanban_view(request):
    qs = Task.objects.all().order_by("priority", "due_date", "title")
    ctx = {
        "todo": qs.filter(status="todo"),
        "doing": qs.filter(status="doing"),
        "done": qs.filter(status="done"),
    }
    return render(request, "tasks/kanban.html", ctx)


# ---------- Calendar ----------

def _month_nav(year: int, month: int):
    first = date(year, month, 1)
    prev_first = (first - timedelta(days=1)).replace(day=1)
    last_day = calendar.monthrange(year, month)[1]
    next_first = (date(year, month, last_day) + timedelta(days=1)).replace(day=1)
    return prev_first.year, prev_first.month, next_first.year, next_first.month


def calendar_view(request):
    today = date.today()
    y = int(request.GET.get("y", today.year))
    m = int(request.GET.get("m", today.month))

    cal = calendar.Calendar(firstweekday=0)
    raw_weeks = cal.monthdayscalendar(y, m)  # list of weeks, days as ints (0 for blanks)

    # Map day -> list[Task] for tasks due in this month
    month_tasks = Task.objects.filter(due_date__year=y, due_date__month=m)
    by_day = {}
    for t in month_tasks:
        by_day.setdefault(t.due_date.day, []).append(t)

    # Build a grid the template can iterate without calling methods:
    # weeks = [ [(d, [tasks...]), ...], ... ]
    weeks = [[(d, by_day.get(d, [])) for d in week] for week in raw_weeks]

    prev_y, prev_m, next_y, next_m = _month_nav(y, m)

    ctx = {
        "year": y,
        "month": m,
        "month_name": calendar.month_name[m],
        "weeks": weeks,
        "prev_y": prev_y,
        "prev_m": prev_m,
        "next_y": next_y,
        "next_m": next_m,
        "weekday_headers": list(calendar.day_name),
    }
    return render(request, "tasks/calendar.html", ctx)
