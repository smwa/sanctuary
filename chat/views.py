from django.http import JsonResponse 
from chat.models import Message
from time import sleep

def index(request):
    if request.method == "GET":
        lastSeenId = int(request.GET.get('lastSeenId', '0'))
        messages = Message.objects.all().filter(id__gt=lastSeenId)

        longPollingSecondsRemaining = 30.0
        SLEEP_INTERVAL = 0.5
        while messages.count() < 1 and longPollingSecondsRemaining > 0.0:
          sleep(SLEEP_INTERVAL)
          longPollingSecondsRemaining -= SLEEP_INTERVAL
          messages = Message.objects.all().filter(id__gt=lastSeenId)

        POPMessages = map(lambda m: {'id': m.id, 'sender': m.sender, 'body': m.body}, messages[0:1000])
        return JsonResponse({'messages': list(POPMessages)})
    if request.method == "POST":
        sender = request.POST.get('sender', None)
        body = request.POST.get('body', None)
        if sender is None or body is None:
            return JsonResponse("Sender and Body are required fields", status=400)
        message = Message(sender=sender, body=body)
        message.save()
        return JsonResponse({'status': 'Ok'})
