from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from thumbs.models import Channel, Thumb
import json

def get_thumbs(request, channel_id):
    """ Returns a json with the last N frames """
    data = []
    channel = Channel.objects.get(id=channel_id)
    thumbs = Thumb.objects.filter(channel=channel).order_by("-datetime")[:120]

    for thumb in thumbs.iterator():
        data.append({
            "id": thumb.id,
            "filepath": thumb.filepath(),
        })

    return HttpResponse(json.dumps(data), content_type="application/json")

def get_thumb(request, thumb_id):
    """ Serves an image """
    try:
        t = get_object_or_404(Thumb, id=thumb_id)
        with open(t.filename) as f:
            content = f.read()
    except OSError:
        return HttpResponse(status=404)
    return HttpResponse(content, content_type="image/jpeg")
