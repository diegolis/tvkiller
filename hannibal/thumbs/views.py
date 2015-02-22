from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from thumbs.models import Channel, Thumb
from sendfile import sendfile
import json

def get_thumbs(request, channel_id):
    """ Returns a json with the last N frames """
    data = []
    channel = Channel.objects.get(id=channel_id)
    thumbs = Thumb.objects.filter(channel=channel).order_by("-datetime")[:120]

    for thumb in thumbs.iterator():
        data.append({
            "id": thumb.id,
            "isodate": thumb.datetime.isoformat(),
        })

    return HttpResponse(json.dumps(data), content_type="application/json")

def get_thumb(request, thumb_id):
    """ Serves an image """
    t = get_object_or_404(Thumb, id=thumb_id)
    return sendfile(request, t.filename.path)
