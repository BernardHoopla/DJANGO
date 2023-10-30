# myapp/models.py
import random

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed


class UserInput(models.Model):
    text_input = models.CharField(max_length=255)


class Leaderboard(models.Model):
    team_name = models.CharField(max_length=100)
    # score = models.PositiveIntegerField()
    score = random.randint(50, 100)
