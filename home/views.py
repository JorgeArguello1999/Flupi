from django.shortcuts import render

from django.contrib.auth.decorators import login_required

# Views from home
@login_required
def home(request):
    return render(request, 'home.html')