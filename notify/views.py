from django.shortcuts import render
from django.shortcuts import redirect
from django.http.response import JsonResponse

from django.contrib.auth.decorators import login_required

from .models import StatusWork

# Notify Front
@login_required
def notify_frontend(request):
    return render(request, 'notify.html')

# Notify Status
def notify_status(request):
    work = StatusWork.objects.filter(id=1).values()[0]

    return JsonResponse({
        "status": work['status']
    })

# Notify Back
@login_required
def notify_backend(request, statuswork):
    """
    Parámetros:
        - statuswork (int): 1 para llamar al técnico, 0 para desactivar.
    Retorna: Redirección a la página 'notify_f'.
    """
    status_obj = StatusWork.objects.get(id=1)

    # Convertir el parámetro a un valor booleano
    if statuswork == 0:
        status_obj.status = False
        status_obj.save()
    if statuswork == 1:
        status_obj.status = True
        status_obj.save()

    return redirect('notify')
