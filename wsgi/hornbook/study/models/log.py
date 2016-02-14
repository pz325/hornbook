from django.db import models


class StudySessionContentLog(models.Model):
    date = models.DateTimeField(auto_now=True)
    session_count = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=200)
    current_deck_contents = models.TextField(blank=True)
    progress_deck_contents = models.TextField(blank=True)
    retired_deck_contents = models.TextField(blank=True)


class StudySessionResultLog(models.Model):
    date = models.DateTimeField(auto_now=True)
    session_count = models.PositiveSmallIntegerField(default=0)
    category = models.CharField(max_length=200)
    grasped_contents = models.TextField()
    new_contents = models.TextField()
