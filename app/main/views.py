from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Home Page')

def profile_view(request):
    return render(request, 'profile.html')

