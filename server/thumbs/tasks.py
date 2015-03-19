#from celery import task
from datetime import datetime
from django.utils import timezone
from django.conf import settings
import os.path

#@task()
def create_videoclip(clip_id, sources, start_time, end_time, filename):
    from thumbs.models import Clip, Origin
    #start_time = timezone.make_aware(datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%Z'), timezone.get_default_timezone())
    #end_time = timezone.make_aware(datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%Z'), timezone.get_default_timezone())

    clip = Clip.objects.get(id=clip_id)
    sources = list(Origin.objects.filter(id__in=sources).order_by('start_time'))

    delta_start = (start_time - sources[0].start_time)
    #delta_end = (sources[-1].end_time - end_time).seconds

    cmd_str = ['ffmpeg', 
                '-y',
                '-i', sources[0].filename.name + '.wmv', 
                '-ss', str(delta_start), 
                '-t', str(end_time - start_time), 
                os.path.join(settings.MEDIA_ROOT, filename)]
    print cmd_str

    import subprocess
    cmd = subprocess.Popen(cmd_str, shell=False)
    stdout, stderr = cmd.communicate()


    if False:

        # the cut of the videos is a long process. it should be done in a celery task.
        if len(sources) == 1:
            clip_video = sources[0].movie.subclip(delta_start, sources[0].duration - delta_end)
        else:
            clip_inicio = sources[0].movie.subclip(delta_start, sources[0].duration)
            clip_fin = sources[-1].movie.subclip(0, sources[-1].duration - delta_end)
            clips_medio = [s.movie for s in sources[1:-1]]
            clip_video = concatenate_videoclips([clip_inicio] + clips_medio + [clip_fin])

        clip_video.write_videofile(os.path.join(settings.MEDIA_ROOT, filename), preset='ultrafast', threads=4)
    
    clip.status = Clip.STATUS.done
    clip.save(update_fields=['status'])
