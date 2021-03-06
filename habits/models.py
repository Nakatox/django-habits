from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User

# Create your models here.

# A user can sign-in¹ (no email validation needed).
# A user can log-in and log-out.
# A user can manage a list of habits².
# One user can't see other user habits, habits can be very personal information.
# A user can easily mark a habit as done when he does it.
# A user can edit or remove a habit.
# A user can see an overview of how well it did the habits.

# A user should easily see what he show do now (habit running late) or if everything's done.

# Read the doc properly, Django already provides a user creation form handling password validation password hashing for you.
# A habit is something like "Run at least once every other day", or "Bake a brioche once a month", "Tech watch twice a week", ...

# So you'll need to find a way, given a habit description and a list of when he did it in the past, to score the user "fitness to the habit".

class Interval(models.Model):
    name = models.CharField(max_length=512)
    def __str__(self):
        return self.name

class Habit(models.Model):
    name = models.CharField(max_length=512)
    content = models.TextField(max_length=1024)
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    days = models.CharField(max_length=10, null=True)
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE, null=True, default='', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class State(models.Model):
    date = models.DateField(auto_now_add=False)
    is_done = models.BooleanField()
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)


