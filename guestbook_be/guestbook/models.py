from django.db import models
from django.utils import timezone

class User(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Entry(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject
