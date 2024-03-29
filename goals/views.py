from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from .models import Goal, Period, goal_mode
from django.utils import timezone


# Create your views here.
@login_required(login_url='login')
def goals(request):
    labels2 = []
    data2 = []
    type = []
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    goals_all_q = Goal.objects.filter(host=request.user)

    for goal in goals_all_q:
        labels2.append(goal.name)
        goal.progress = round((goal.goal_done / goal.goal) * 100)
        data2.append(goal.progress)

    context = {'goals': goals_all_q, 'labels': labels2, 'data': data2, 'type': type}
    return render(request, 'goals/index.html', context)

@login_required(login_url='login')
def createGoal(request):
    periods = Period.objects.all()
    modes = goal_mode.objects.all()

    if request.method == 'POST':
        period_name = request.POST.get('period')
        period, created = Period.objects.get_or_create(name=period_name)

        mode_name = request.POST.get('mode')
        mode, created = goal_mode.objects.get_or_create(name=mode_name)

        Goal.objects.create(
            host=request.user,
            name=request.POST.get('name'),
            desc=request.POST.get('desc'),
            goal=request.POST.get('goal'),
            period=period,
            mode=mode,
        )
        return redirect('goals')
    context = {'periods': periods, 'modes': modes}
    return render(request, 'goals/goal_form.html', context)

@login_required(login_url='login')
def goalprogress(request, pk):
    goal = Goal.objects.get(id=pk)
    goal.progress = round((goal.goal_done / goal.goal) * 100)
    if request.user != goal.host:
        return HttpResponse('شما اجازه ورود به این صفحه را ندارید')

    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        goal_done = request.POST.get('goal-done')
        goal.name = name
        goal.desc = desc
        goal.goal_done = goal_done
        goal.save()
        return redirect('goals')

    return render(request, 'goals/goal_add.html', {'goal': goal})


def deleteGoal(request, pk):
    goal = Goal.objects.get(id=pk)

    if request.user != goal.host:
        return HttpResponse('شما اجازه ورود به این صفحه را ندارید')

    goal.delete()
    return redirect('goals')

    return render(request, 'goals/delete.html', {'obj': goal})
