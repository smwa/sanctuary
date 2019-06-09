from django.http import JsonResponse 
from chat.models import Message
from time import sleep
from django.conf import settings

def index(request):
    if request.method == "GET":
        lastSeenId = int(request.GET.get('lastSeenId', '0'))
        messages = Message.objects.all().filter(id__gt=lastSeenId).order_by('id')

        longPollingSecondsRemaining = 30.0
        SLEEP_INTERVAL = 0.5
        while messages.count() < 1 and longPollingSecondsRemaining > 0.0:
          sleep(SLEEP_INTERVAL)
          longPollingSecondsRemaining -= SLEEP_INTERVAL
          messages = Message.objects.all().filter(id__gt=lastSeenId).order_by('id')

        POPMessages = map(lambda m: {'id': m.id, 'sender': m.sender, 'body': m.body}, messages[0:1000])
        return JsonResponse({'messages': list(POPMessages)})
    if request.method == "POST":
        sender = request.POST.get('sender', None)
        body = request.POST.get('body', None)
        if sender is None or body is None:
            return JsonResponse("Sender and Body are required fields", status=400)
        message = Message(sender=sender, body=body)
        message.save()

        # Limit total messages
        messages = Message.objects.all().order_by('id')
        count = messages.count()
        diff = count - settings.CHAT_MAX_MESSAGES
        if diff > 0:
          for i in range(diff):
            message = messages[0]
            message.delete()
          
        return JsonResponse({'status': 'Ok'})
