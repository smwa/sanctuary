from django.http import JsonResponse 
from files.models import Hash, File
from time import sleep

def list(request):
    files = File.objects.all()
    ret = []
    for file in files:
        ret.append({
            'filename': file.label,
            'size': file.hash.size,
            'hash': file.hash.md5
        })

    return JsonResponse({'files': ret})
