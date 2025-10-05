#Here's where what happens when someone hits a URL
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Q
import csv

from .models import Task
from .forms import TaskForm

#The homepage. Grabs tasks from the database, applies any filters/sorting from the query string 
def list_view(request):
    order = request.GET.get("order", "due")
    qs = Task.objects.all()
    if order == "priority":
        # high > med > low
        priority_weight = {"high": 3, "med": 2, "low": 1}
        qs = sorted(qs, key=lambda t: (-priority_weight.get(t.priority,0), t.due_date or ""))
    elif order == "created":
        qs = Task.objects.order_by("-created_at")
    else:
        qs = Task.objects.order_by("due_date", "title")

    stats = {
        "total": Task.objects.count(),
        "todo": Task.objects.filter(status="todo").count(),
        "doing": Task.objects.filter(status="doing").count(),
        "done": Task.objects.filter(status="done").count(),
    }
    return render(request, "tasks/list.html", {"tasks": qs, "stats": stats, "order": order})

#Shows the form on GET, saves a new taks on POST, then sends you back home 
def create_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks:list")
    else:
        form = TaskForm()
    return render(request, "tasks/form.html", {"form": form})

#Kinda same as create, but prefilled. Great for changing status/priority 
def update_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/form.html", {"form": form, "task": task})

#Where it asks if you're sure to delete the task (GET), then actually delete on POST
def delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("tasks:list")
    return render(request, "tasks/confirm_delete.html", {"task": task})

#Lightweight action from the list/Kanban. Flips done/undone (or steps status) and jumps back to where you came from.
def toggle(request, pk):
    """Toggle done <-> todo (leaves 'doing' alone)."""
    if request.method != "POST":
        return redirect("tasks:list")
    task = get_object_or_404(Task, pk=pk)
    task.status = "todo" if task.status == "done" else "done"
    task.save(update_fields=["status"])
    return redirect("tasks:list")

#Splits tasks into three neat columns (todo/doing/done) so progress is obvious
def kanban_view(request):
    return render(
        request,
        "tasks/kanban.html",
        {
            "todo": Task.objects.filter(status="todo").order_by("due_date"),
            "doing": Task.objects.filter(status="doing").order_by("due_date"),
            "done": Task.objects.filter(status="done").order_by("due_date"),
        },
    )

#Streams a CSV to the browser so you can sort/filter in Excel/Sheets
def export_csv(request):
    """Export all tasks (respects ?order= like list)."""
    order = request.GET.get("order", "due")
    qs = Task.objects.all()
    if order == "priority":
        priority_order = {"high": 3, "med": 2, "low": 1}
        qs = sorted(qs, key=lambda t: (-priority_order.get(t.priority,0), t.due_date or ""))
    elif order == "created":
        qs = Task.objects.order_by("-created_at")
    else:
        qs = Task.objects.order_by("due_date", "title")

    resp = HttpResponse(content_type="text/csv")
    resp["Content-Disposition"] = 'attachment; filename="tasks.csv"'
    w = csv.writer(resp)
    w.writerow(["Title", "Description", "Due date", "Priority", "Status", "Created"])
    for t in qs:
        w.writerow([t.title, t.description, t.due_date or "", t.get_priority_display(), t.get_status_display(), t.created_at.strftime("%Y-%m-%d %H:%M")])
    return resp
