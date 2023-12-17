from django.shortcuts import render

# Views from home
def home(request):
    return render(request, 'home.html')