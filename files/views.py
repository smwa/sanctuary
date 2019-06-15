from django.http import JsonResponse, HttpResponse
from django.conf import settings
from files.models import Hash, File
from time import sleep
import hashlib
import os
import mimetypes

for hash in Hash.objects.all():
  if not os.path.isfile(hash.content.path):
    for file in hash.file_set.all():
      file.delete()
    hash.content.delete()
    hash.delete()

def files(request):
  if request.method == 'GET':
    return _get(request)
  else:
    return _post(request)

def _get(request):
    lastSeenId = int(request.GET.get('lastSeenId', 0))
    files = File.objects.all().filter(id__gt=lastSeenId).order_by('id')

    longPollingSecondsRemaining = 30.0
    SLEEP_INTERVAL = 0.5
    while files.count() < 1 and longPollingSecondsRemaining > 0.0:
      sleep(SLEEP_INTERVAL)
      longPollingSecondsRemaining -= SLEEP_INTERVAL
      files = File.objects.all().filter(id__gt=lastSeenId).order_by('id')

    ret = []
    for file in files[0:1000]:
      ret.append({
        'name': file.label,
        'size': file.hash.size,
        'hash': file.hash.md5,
        'id': file.id
      })
    return JsonResponse({'files': ret})

def _post(request):
  for f in request.FILES.getlist('fileInput[]'):
    md5 = hashlib.md5()
    for chunk in f.chunks():
      md5.update(chunk)
    hash = Hash(content=f, md5=md5.hexdigest(), size=f.size)
    try:
      existingHash = Hash.objects.get(md5=hash.md5)
      hash = existingHash
    except Hash.DoesNotExist:
      hash.save()
    file = File(label=f.name, hash=hash)
    try:
      existingFile = File.objects.get(label=file.label, hash__md5=hash.md5)
      file = existingFile
    except File.DoesNotExist:
      file.save()
    _deleteFilesIfLowOnSpace()
    return JsonResponse({'status': 'Ok'})
  return JsonResponse({'errors': form.errors}, status=400)

def download(request, id):
  file = None
  try:
    file = File.objects.get(id=id)
  except File.DoesNotExist:
    return HttpResponse("Invalid file", status=400)
  filename = os.path.basename(file.label)
  contentType = mimetypes.guess_type(filename)
  response = HttpResponse(file.hash.content, content_type=contentType[0])
  response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
  return response

def _deleteFilesIfLowOnSpace():
  hashes = Hash.objects.all().order_by("id")
  while _freeSpaceInGb < settings.MINIMUM_FREE_SPACE_GB and len(hashes) > 0:
    hash = hashes[0]
    hashes = hashes[1:]
    for file in hash.file_set.all():
      file.delete()
    hash.content.delete()
    hash.delete()

def _freeSpaceInGb()
  statvfs = os.statvfs(settings.BASE_DIR)
  freespace = statvfs.f_frsize * statvfs.f_bfree
  freespaceGB = freespace / (1024.0 * 1024.0 * 1024.0)
