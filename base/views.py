from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import MyUserCreationForm
from .models import studySummary, Topic
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
@login_required(login_url='login')
def homePage(request):
    labels = []
    data = []
    posts_q = Topic.objects.filter(host=request.user)
    for city in posts_q:
        labels.append(city.name)
        data.append(city.data)

    def _sum(arr):

        # initialize a variable
        # to store the sum
        # while iterating through
        # the array later
        arr_sum = 0

        # iterate through the array
        # and add each element to the sum variable
        # one at a time
        for i in arr:
            arr_sum = arr_sum + i

        return (arr_sum)

    ans = _sum(data)
    try:
        data_average = (ans / len(data))
    except:
        data_average = 0
    context = {'labels': labels, 'data': data, 'data_avg': data_average, 'ans': ans}
    return render(request, 'base/index.html', context)


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
        return redirect('home')

    return render(request, 'base/register.html', {'form': form})


def logoutPage(request):
    logout(request)
    return redirect('home')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'نام کاربری وجود ندارد')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور ناموجود است')

    return render(request, 'base/login.html')
