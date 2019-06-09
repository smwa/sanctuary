from django.http import JsonResponse 
from files.models import Hash, File
from time import sleep

def list(request):
    return JsonResponse({})
