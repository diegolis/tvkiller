from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from thumbs.models import Channel, Thumb, Clip
from sendfile import sendfile
from datetime import timedelta

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

    return JsonResponse(data, safe=False)


def get_thumb(request, thumb_id):
    """ Serves an image """
    t = get_object_or_404(Thumb, id=thumb_id)
    return sendfile(request, t.filename.path)

def make_clip(request, thumb_id, duration):
    """
    Server the link to the video.
    """
    thumb = get_object_or_404(Thumb, id=thumb_id)
    clip = Clip.create_from_channel(thumb.channel, thumb.datetime, thumb.datetime + timedelta(seconds=int(duration)))
    return JsonResponse({'clip_url':request.build_absolute_uri(clip.get_absolute_url())})



def player(request, hashid):
    """the page to view a clip"""
    clip = get_object_or_404(Clip, hashid=hashid)
    return render(request, 'player.html', {'clip': clip})
