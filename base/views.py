from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import MyUserCreationForm
from .models import studySummary, Topic, chek
from goals.models import Goal
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta


# Create your views here.
@login_required(login_url='login')
def homePage(request):
    labels = []
    data = []
    label_all = []
    data_all = []
    page = []
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    posts_q = Topic.objects.filter(host=request.user, created__gte=thirty_days_ago)
    post_all_q = Topic.objects.filter(host=request.user)

    for city in posts_q:
        labels.append(city.name)
        data.append(city.data)
        page.append(city.page)

    for city in post_all_q:
        label_all.append(city.name)
        data_all.append(city.data)

    try:
        # Retrieve the user's Google account
        account = SocialAccount.objects.get(user=request.user, provider='google')
        # Retrieve the user's profile picture URL
        profile_picture_url = account.extra_data['picture']
    except SocialAccount.DoesNotExist:
        # Handle the case where the user is not authenticated with Google
        profile_picture_url = None

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

    if data:
        message_if_0 = ''
    else:
        message_if_0 = 'اضافه کردن ساعت مطالعه'

    ans = _sum(data)
    ans_all = _sum(data_all)
    page_all_week = _sum(page)
    last_ten_goals = Goal.objects.filter().order_by('-id')[:2]
    try:
        data_average = (ans / len(data))
    except:
        data_average = 0
    context = {'labels': labels, 'data': data, 'data_avg': data_average, 'ans': ans, 'msgnn': message_if_0,
               'profile_picture_url': profile_picture_url, 'page': page_all_week, 'goals': last_ten_goals}
    return render(request, 'base/index.html', context)


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        email = request.POST.get('email').lower()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            # Try to retrieve a user with the given email
            user = User.objects.get(username=username)
            # If a user exists with the given email, return an error message
            messages.error(request, 'نام کاربری تکراری است')
        except User.DoesNotExist:
            if password1 == password2:
                try:
                    user = User.objects.get(email=email)
                    messages.error(request, 'ایمیل تکراری است')
                except User.DoesNotExist:
                    user = User.objects.create_user(username, email, password1)
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    user.save()
                    login(request, user)
                    return redirect('home')
            else:
                messages.error(request, 'رمز عبور ها با هم مطابقت ندارند')

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
        user = User.objects.get(username=username)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور ناموجود است')

    return render(request, 'base/login.html')


@login_required(login_url='login')
def createTopic(request):
    if request.method == 'POST':
        time = request.POST.get('time'),

        time_string = time[0]

        # Split the time string into hour and minute components
        hour, minute = time_string.split(":")

        # Convert the minute component to an integer
        minute = int(minute)

        # Round the minute component up or down
        if minute < 30:
            minute = 0
        else:
            minute = 60

            # Increment the hour component
            hour = str(int(hour) + 1)

        # Combine the hour and minute components into a new time string
        rounded_time_string = hour + ":" + str(minute).zfill(2)

        print("Original time: ", time_string)
        print("Rounded time: ", rounded_time_string)

        hourround, minuteround = rounded_time_string.split(":")

        print("Rounded hour: ", hourround)

        Topic.objects.create(
            host=request.user,
            name=request.POST.get('name'),
            data=hourround,
            page=request.POST.get('page'),
        )

        return redirect('home')

    return render(request, 'base/topic_form.html')
