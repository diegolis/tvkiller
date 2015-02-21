from django.shortcuts import render
from django.http import HttpResponse
from thumbs.models import Channel, Thumb
import json

def get_thumbs(request, channel_id):
    data = []
    channel = Channel.objects.get(id=channel_id)
    thumbs = Thumb.objects.filter(channel=channel).order_by("-id")[:10]

    for thumb in thumbs.iterator():
        data.append({
            "id": thumb.id,
            "filepath": thumb.filepath(),
        })

    return HttpResponse(json.dumps(data), content_type="application/json")
