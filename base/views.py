from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import MyUserCreationForm
from .models import studySummary
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.
def homePage(request):
    labels = []
    data = []
    posts_q = studySummary.objects.all()
    for city in posts_q:
        labels.append(city.title)
        data.append(city.data)

    context = {'labels': labels, 'data': data}
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
        else:
            messages.error(request, 'نام کاربری یا رمز عبور ناموجود است')
        

    return render(request, 'base/login.html')