from django.db import migrations
from habits.models import Interval


def createInterval(apps, schema_editor):
    Interval.objects.create(id = 1,name = "1 time per week")
    Interval.objects.create(id = 2,name = "1 time per day")
    Interval.objects.create(id = 3,name = "every day (except weekends)")

class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(createInterval)
    ]
