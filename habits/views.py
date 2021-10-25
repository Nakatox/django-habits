from django.shortcuts import render, redirect
from django import forms
from habits.models import Habit, Interval, State 

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from datetime import date, timedelta
import datetime



# Create your views here.

def index(request):
    if request.user is not None:

        nbDone = {}
        nbState = {}
        stats = {}

        habits = Habit.objects.filter(user_id = request.user.id)

        tab = []
        for habit in habits:
            tab += State.objects.filter(habit_id = habit.id)
            nbDone.update({habit.id:{}})
            nbState.update({habit.id:{}})

        is_done = State.objects.filter(habit_id = habits)
        today = date.today()

        everyDay = Interval.objects.get(id = 2)
        everyDayEWeek = Interval.objects.get(id = 3)
        everyWeeks = Interval.objects.get(id = 1)

        timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        startTime = datetime.datetime.strptime(timenow,'%Y-%m-%d %H:%M:%S')

        weeksOfState = {}
        timeLeft = {}
        
        for e in tab:
            a = e.date
            d = " 23:59:59"
            c = f'{str(a)}{d}'
            b = same_week(a, today)
            if e.date <= today:
                nbState[e.habit_id].update({e.id: e.is_done})
            if e.is_done == 1:
                nbDone[e.habit_id].update({e.id: e.is_done})

            nbDone.update({})
            weeksOfState.update({ a : b })
            timeLeft.update({e.id : str(datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S') - startTime)})

        for habit in habits:
            if len(nbState[habit.id]) > 0:
                stats.update({habit.id : (len(nbDone[habit.id])*100)/len(nbState[habit.id])})
            else:
                stats.update({habit.id : 0})

    return render(request, "habits/index.html",{'stats':stats,'timeLeft':timeLeft,'everyDay': everyDay,'everyDayEWeek':everyDayEWeek,'everyWeeks':everyWeeks,'habits': habits, 'is_done':is_done, 'tab':tab, 'date_now': today, 'weeksOfState': weeksOfState})


def delete(request):
    if request.method == 'POST' and request.user is not None:
        a = Habit.objects.filter(id=request.GET.get('id'))
        a.delete()
    return redirect('home')


def check(request):
    if request.method == 'POST' and request.user is not None:
        a = State.objects.get(pk = request.GET.get('id'))
        a.is_done = request.GET.get('is_done')
        a.save()
    
    return redirect('home')


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def same_week(date1, date2):
    return date1.isocalendar()[1] == date2.isocalendar()[1] \
              and date1.year == date2.year

def addHabit(request):
    if request.user is not None:
        if request.method == 'POST':
            if request.POST.get('interval') == "none":
                request.POST._mutable = True
                request.POST['interval'] = None
            form = addHabitForm(request.POST)
            interval2 = form['interval'].value()
            days = request.POST.getlist('days[]')
            print(type(request.POST.get('interval')))
            if form.is_valid():

                name = form.cleaned_data.get('name')
                content = form.cleaned_data.get('content')
                start_date = form.cleaned_data.get('start_date')
                end_date = form.cleaned_data.get('end_date')
                interval = form.cleaned_data.get('interval')

                # We add the values to a new habit
                habitCreated = Habit.objects.create(name = name, content = content, start_date = start_date, end_date = end_date, days = " ".join(days), interval = interval, user_id = request.user.id)

                habitCreated.save()

                # we add for each day or week a state of the habit
                for single_date in daterange(start_date, end_date):
                    if days:
                        for e in days:
                            if int(e) == single_date.weekday():
                                State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = habitCreated.id)
                    elif interval2 != "none":
                        if interval2 == "2":
                            State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = habitCreated.id)
                        elif interval2 == "1":
                            if single_date.weekday() == 6:
                                State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = habitCreated.id)
                        elif interval2 == "3":
                            if not single_date.weekday() == 6 and not single_date.weekday() == 5:
                                State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = habitCreated.id)

                return redirect('home')
        else:
            form = addHabitForm
    else:
        return redirect('home')

    return render(request, "habits/addHabit.html",{'form': addHabitForm})


def modifHabit(request):
    if request.GET.get('id') is not None:
        id_habit = request.GET.get('id')
    else:
        id_habit = request.POST.get('id_habit')

    if request.user is not None and Habit.objects.get(id = id_habit).user_id == request.user.id:
        habit = Habit.objects.get(id = id_habit)

        if habit.interval is not None:
            habit_interval = Interval.objects.get(name = habit.interval).id
        else:
            habit_interval = ""

        start_date = habit.start_date.strftime("%Y-%m-%d")
        end_date = habit.end_date.strftime("%Y-%m-%d")
        data = {"name": habit.name,"content":habit.content,"start_date":start_date,"end_date":end_date,"interval":habit_interval}
        
        if request.method == 'POST':
            form = addHabitForm(request.POST)
            interval2 = form['interval'].value()
            days = request.POST.getlist('days[]')

            if request.POST.get('interval') == "none":
                request.POST._mutable = True
                request.POST['interval'] = None
            
            if form.is_valid():
                state_checked = {}
                Habit.objects.filter(id = id_habit).update(name = form.cleaned_data.get('name'),content = form.cleaned_data.get('content'),start_date = form.cleaned_data.get('start_date'),end_date = form.cleaned_data.get('end_date'),interval = form.cleaned_data.get('interval'),days = " ".join(days))
                
                for i in State.objects.filter(habit_id = id_habit):
                    if i.is_done == 1: 
                        state_checked.update({i.date : i.date })
                
                State.objects.filter(habit_id=id_habit).delete()


                for single_date in daterange(form.cleaned_data.get('start_date'), form.cleaned_data.get('end_date')):
                    if days:
                        for e in days:
                            if int(e) == single_date.weekday():
                                if single_date in state_checked:
                                    State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 1, habit_id = id_habit)
                                else:
                                    State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = id_habit)
                    elif interval2 != "none":  
                        if interval2 == "2":
                            if single_date in state_checked:
                                State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 1, habit_id = id_habit)
                            else:
                                State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = id_habit)
                        elif interval2 == "1":
                            if single_date.weekday() == 6:
                                if single_date in state_checked:
                                    State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 1, habit_id = id_habit)
                                else:
                                    State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = id_habit)
                        elif interval2 == "3":
                            if not single_date.weekday() == 6 and not single_date.weekday() == 5:
                                if single_date in state_checked:
                                    State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 1, habit_id = id_habit)
                                else:
                                    State.objects.create(date = single_date.strftime("%Y-%m-%d"), is_done = 0, habit_id = id_habit)


                return redirect('home')
        else:
            form = addHabitForm
    else:
        return redirect('home')

    return render(request, "habits/modifHabit.html",{'form': addHabitForm,"id_habit":id_habit,"habit":habit,"data":{1: data["name"],2:data["content"],3:data["start_date"],4:data["end_date"],5:data["interval"]}})


class DateInput(forms.DateInput):
    input_type = 'date'


class addHabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ('name', 'content', 'start_date', 'end_date', 'interval')
        widgets = {
            'end_date': DateInput(),
            'start_date': DateInput(),
        }


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})