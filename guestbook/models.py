from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.name


class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.subject
