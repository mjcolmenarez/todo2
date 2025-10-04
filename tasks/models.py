from django.db import models

class Task(models.Model):
    PRIORITY_CHOICES = [("low","Low"), ("med","Medium"), ("high","High")]
    STATUS_CHOICES = [("todo","To do"), ("doing","Doing"), ("done","Done")]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default="med")
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default="todo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        return self.title
