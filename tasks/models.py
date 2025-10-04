from django.db import models

class Task(models.Model):
    STATUS_TODO = 'todo'
    STATUS_DOING = 'doing'
    STATUS_DONE = 'done'
    STATUS_CHOICES = [
        (STATUS_TODO, 'To do'),
        (STATUS_DOING, 'In progress'),
        (STATUS_DONE, 'Done'),
    ]

    PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Normal'),
        (3, 'Low'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_TODO)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status', 'priority', 'due_date', '-created_at']

    def __str__(self):
        return self.title
