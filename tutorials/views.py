# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import courses, Video, VideoWatchProgress, Comment
from django.db.models import Q
import logging
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import re
from datetime import timedelta
from django.utils import timezone


def HomePage(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    price = request.GET.get('price')
    print(price)
    time = request.GET.get('time')
    itemsFiltered = []

    # Implement search functionality
    if q:
        items = courses.objects.filter(
            Q(title__icontains=q)
        )
    else:
        items = courses.objects.all()

    # Filter by price

    if price == 'free':
        items = items.filter(price=0)
    elif price == 'paid':
        items = items.exclude(price=0)

        # Apply filtering based on time
    if time == 'recent':
        items = items.order_by('-created')
    elif time == 'oldest':
        items = items.order_by('created')
    elif time == 'all' or time == None:
        # No time-based filtering, display all itemsFiltered
        items = items.all()

    context = {'coureses': items}
    return render(request, 'tutorials/main.html', context)


def tutorial_detail(request, tutorial_id):
    tutorial = get_object_or_404(courses, id=tutorial_id)
    tutorial_comments = tutorial.comment_set.all()
    videos = tutorial.video_set.all()

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            courses=tutorial,
            content=request.POST.get('body')
        )
    return render(request, 'tutorials/tutorial_detail.html',
                  {'tutorial': tutorial, 'videos': videos, 'course_comment': tutorial_comments})


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'tutorials/video_detail.html', {'video': video})


def update_video_progress(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user
    # Assuming progress is in "minutes:seconds" format
    progress = request.GET.get('progress')

    # Retrieve or create the VideoWatchProgress instance

    # Parse the existing progress from the database

    # Parse the current progress received from the request
    current_minutes, current_seconds = map(
        int, progress.split(':')) if progress else (0, 0)

    # Calculate the total progress in seconds
    total_current_seconds = current_minutes * 60 + current_seconds
    total_updated_seconds = total_current_seconds

    # Calculate the updated progress in hours:minutes:seconds format
    updated_hours, remaining_minutes = divmod(total_updated_seconds, 3600)
    updated_minutes, updated_seconds = divmod(remaining_minutes, 60)

    # Format the updated progress as "hours:minutes:seconds"
    updated_progress = f"{updated_hours:02d}:{updated_minutes:02d}:{updated_seconds:02d}"
    print(updated_progress)
    # Save the updated progress to the instance and the database

    # splited_updated_progress = updated_progress.split(':')
    # splited_existing_data = video_progress.progress.split(':')
    # last_seconds = int(
    #     splited_updated_progress[2]) + int(splited_existing_data[2])
    # last_minutes = int(
    #     splited_updated_progress[1]) + int(splited_existing_data[1])
    # last_hours = int(
    #     splited_updated_progress[0]) + int(splited_existing_data[0])

    # last_progress = f"{last_hours:02d}:{last_minutes:02d}:{last_seconds:02d}"
    # print(last_progress)

    # video_progress.progress = updated_progress
    video_progress, created = VideoWatchProgress.objects.get_or_create(
        user=user, progress=updated_progress, video=video, created=timezone.now())
    # video_progress.save()

    return JsonResponse({'status': 'success'})
