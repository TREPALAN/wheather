from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, render
from rest_framework.response import Response
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
load_dotenv()

from .models import Wheather
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # Get the API key from the .env file
        API_KEY = os.getenv("API_KEY")
        return render(request, "app/index.html",
                      {"API_KEY": API_KEY}
                      )
    else:
        return HttpResponseRedirect(reverse("login"))


def wheather(request, city):
    # Load Data from Local Storage
    if request.method != 'GET':
        return HttpResponse(status=405)
    data =  Wheather.objects.filter(city=city.replace("+", " ")).order_by('-created_at').first()
    if data is None:
        return JsonResponse({"status": "Server Error"}, status=404)
    return JsonResponse(data.serialize(), safe=False, status=200)


@csrf_exempt
def cache(request):
    # Save and load Data in Local Storage
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    data = json.loads(request.body)
    city = data['name']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    temperature = data['main']['temp']
    visibility = data['visibility']
    wind_speed = data['wind']['speed']
    icon = data['weather'][0]['icon']

    object =  Wheather(city=city, feels_like=feels_like, humidity=humidity, pressure=pressure, temperature=temperature, visibility=visibility, wind_speed=wind_speed, icon=icon)
    try:
        object.save()
    except(IntegrityError):
         Wheather.objects.filter(city=city).update(city=city, feels_like=feels_like, humidity=humidity, pressure=pressure, temperature=temperature, visibility=visibility, wind_speed=wind_speed, icon=icon)
         object = Wheather.objects.filter(city=city).order_by('-created_at').first()
    return JsonResponse(object.serialize(), safe=False, status=200)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "app/register.html", {
                "message": "username address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "app/register.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))