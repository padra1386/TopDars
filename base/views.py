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
from tutorials import models
from .forms import UserForm


# Create your views here.
@login_required(login_url='login')
def homePage(request):
    labels = []
    data = []
    label_all = []
    data_all = []
    page = []
    # Get the current date and time
    current_date = timezone.now()

    # Calculate the start and end of the current day
    start_of_day = datetime(current_date.year, current_date.month, current_date.day)
    end_of_day = start_of_day + timedelta(days=1)

    # Calculate the start and end dates for the last 30 days
    start_date = timezone.now() - timezone.timedelta(days=30)
    end_date = start_date - timedelta(days=30)

    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    progress_data = models.VideoWatchProgress.objects.filter(user=request.user, created__gte=start_date)
    progress_data_day = models.VideoWatchProgress.objects.filter(user=request.user,
                                                                 created__range=(start_of_day, end_of_day))

    posts_q = Topic.objects.filter(
        host=request.user, created__gte=thirty_days_ago)
    post_all_q = Topic.objects.filter(host=request.user)

    for city in progress_data:
        split_data = city.progress.split(':')
        minute_to_seconds = (split_data[1] * 60)
        seconds = split_data[2]
        sum2 = int(minute_to_seconds) + int(seconds)
        labels.append(city.video.title)
        data.append(sum2)


    # for city in progress_data:
    #     label_all.append(city.video.title)
    #     data_all.append(city.progress)

    try:
        # Retrieve the user's Google account
        account = SocialAccount.objects.get(
            user=request.user, provider='google')
        # Retrieve the user's profile picture URL
        profile_picture_url = account.extra_data['picture']
    except SocialAccount.DoesNotExist:
        # Handle the case where the user is not authenticated with Google
        profile_picture_url = None

        def sum_times(user_times):
            total_time = timedelta()

            for time_str in user_times:
                hours, minutes, seconds = map(int, time_str.progress.split(':'))
                time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
                total_time += time_delta

            return total_time

    total_time_day = sum_times(progress_data_day)
    total_time = sum_times(progress_data)

    print(data)

    def calculate_average(user_times):
        total_time = timedelta()

        for time_str in user_times:
            hours, minutes, seconds = map(int, time_str.progress.split(':'))
            time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            total_time += time_delta

        num_times = len(user_times)
        if num_times > 0:
            average_time = total_time / num_times
            # Round the average time to the nearest whole second
            average_time = timedelta(seconds=round(average_time.total_seconds()))
        else:
            average_time = timedelta()

        return average_time

    average_time_day = calculate_average(progress_data_day)
    average_time = calculate_average(progress_data)
    print(average_time_day)

    # def _sum(arr):

    #     # initialize a variable
    #     # to store the sum
    #     # while iterating through
    #     # the array later
    #     arr_sum = 0

    #     # iterate through the array
    #     # and add each element to the sum variable
    #     # one at a time
    #     for i in arr:
    #         arr_sum = arr_sum + i

    #     return (arr_sum)

    if data:
        message_if_0 = ''
    else:
        message_if_0 = 'دیدن دوره ها'

    # ans = _sum(data)
    # ans_all = _sum(data_all)
    # page_all_week = _sum(page)
    last_ten_goals = Goal.objects.filter(host=request.user).order_by('-id')[:2]
    # for data in progress_data:
    #     split_data = data.progress.split(':')
    #     minute_to_seconds = (split_data[1] * 60)
    #     seconds = split_data[2]
    #     sum = int(minute_to_seconds) + int(seconds)

    # try:
    #     data_average = (ans / len(data))
    # except:
    #     data_average = 0
    context = {'labels': labels, 'data_day': total_time_day, 'data': total_time, 'datachart': data, 'data_avg_day': average_time_day,
               'data_avg': average_time, 'msgnn': message_if_0,
               'profile_picture_url': profile_picture_url, 'goals': last_ten_goals, 'progress': progress_data}
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
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/update-user.html', {'form': form})



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
