from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import Schedule
from .serializers import UserSerializer, ScheduleSerializer
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("<h1>Hello, Flight Scheduler!</h1>")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# /flights/ APIs
# Get all
@csrf_exempt
def flight_list(request):
    if request.method == 'GET':
        schedules = Schedule.objects.all()
        schedules_serializer = ScheduleSerializer(schedules, many=True)
        return JsonResponse(schedules_serializer.data, safe=False)

    # Add one
    if request.method == 'POST':
        schedule_data = JSONParser().parse(request)
        schedule_serializer = ScheduleSerializer(data=schedule_data)
        if schedule_serializer.is_valid():
            schedule_serializer.save()
            return JsonResponse(schedule_data.data, status=status.HTTP_201_CREATED)
        return JsonResponse(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete all
    if request.method == 'DELETE':
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def flight_detail(request, pk):
    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # Retrieve one record
    if request.method == 'GET':
        schedule_serializer = ScheduleSerializer(schedule)
        return JsonResponse(schedule_serializer.data)

    # Update one record
    if request.method == 'PUT':
        schedule_data = JSONParser().parse(request)
        schedule_serializer = ScheduleSerializer(schedule, data=schedule_data)
        if schedule_serializer.is_valid():
            schedule_serializer.save()
            return JsonResponse(schedule_serializer.data)
        return JsonResponse(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete one record
    if request.method == 'DELETE':
        schedule.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
