from django.contrib import admin
from django.contrib.admin.decorators import display
from habits.models import Habit, State, Interval

# Register your models here.

# admin.site.register(Website)
# admin.site.register(Check)

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "content", "start_date", "end_date")
    search_fields = ['name']
    

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("date","is_done", "habit")
    autocomplete_fields = ["habit"]

@admin.register(Interval)
class IntervalAdmin(admin.ModelAdmin):
    # list_display = ("name")
    display = "name"

