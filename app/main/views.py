from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Home Page')
@login_required
def profile_view(request):
    return render(request, 'profile.html')

