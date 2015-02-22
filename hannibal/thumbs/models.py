from django.db import models
from django.db.models import Q
from django.conf import settings
import os
from django.db.models import permalink
from datetime import timedelta
from moviepy.editor import VideoFileClip, concatenate_videoclips
from model_utils.fields import StatusField
from model_utils import Choices
from hashids import Hashids


hashids = Hashids(settings.HASHID_SALT, 10)


# Create your models here.
class Channel(models.Model):
    """
    Model to represent TV Channel

    device_name & device_slot reference recording technologies
    """

    name = models.CharField(max_length=200, unique=True)
    device_name = models.CharField(max_length=200, default="")
    device_slot = models.CharField(max_length=200, default="")

    # def save(self, *args, **kwargs):
        # """ Create a directory for the thumbnails. """
        # super(Channel, self).save(*args, **kwargs)
        # try:
            # os.mkdir(self.base_dir())
        # except OSError:
            # pass

    def __unicode__(self):
        return self.name


class BaseVideo(models.Model):

    class Meta:
        abstract = True

    channel = models.ForeignKey(Channel)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    filename = models.FileField()

    def __unicode__(self):
        return unicode(self.filename)

    @property
    def movie(self):
        """return a moviepy clip object"""
        return VideoFileClip(self.filename.path)

    @property
    def duration(self):
        return self.movie.duration

    def save(self, *args, **kwargs):
        self.end_time = self.start_time + timedelta(seconds=self.duration)
        return super(BaseVideo, self).save(*args, **kwargs)


class Origin(BaseVideo):
    """a chunk of video captured from a channel.
    It's the source for clips"""
    pass


class Clip(BaseVideo):
    """a videoclip generated cutting/concatenating
    origin videos"""

    STATUS = Choices('in_process', 'done')
    hashid = models.CharField(max_length=10, unique=True, editable=False)
    status = StatusField()


    @permalink
    def get_absolute_url(self):
        return ("player", [self.hashid])

    def save(self, *args, **kwargs):

        self.hashid = hashids.encode(*map(ord, str(self.filename)))
        return super(Clip, self).save(*args, **kwargs)

    @classmethod
    def create_from_channel(cls, channel, start_time, end_time):
        """
        create (if needed) a clip instance for the channel and time segment given
        """
        # don't duplicate a clip already generated
        clip = Clip.objects.filter(channel=channel, start_time=start_time, end_time=end_time)
        if clip:
            return clip[0]

        sources = list(Origin.objects.filter(Q(start_time__range=(start_time, end_time)) |
                                             Q(end_time__range=(start_time, end_time)) |
                                             Q(start_time__lte=start_time, end_time__gte=end_time)))

        if not sources:
            return None

        delta_start = (start_time - sources[0].start_time).seconds
        delta_end = (sources[-1].end_time - end_time).seconds


        # the cut of the videos is a long process. it should be done in a celery task.
        if len(sources) == 1:

            clip_video = sources[0].movie.subclip(delta_start, sources[0].duration - delta_end)
        else:
            clip_inicio = sources[0].movie.subclip(delta_start, sources[0].duration)
            clip_fin = sources[-1].movie.subclip(0, sources[-1].duration - delta_end)
            clips_medio = [s.movie for s in sources[1:-1]]
            clip_video = concatenate_videoclips([clip_inicio] + clips_medio + [clip_fin])


        filename = '%s_%s_%s.webm' % (channel.name, start_time.strftime("%Y%m%d%H%M%S"),
                                      end_time.strftime("%Y%m%d%H%M%S"))

        clip_video.write_videofile(os.path.join(settings.MEDIA_ROOT, filename), preset='ultrafast', threads=4)
        clip = Clip.objects.create(channel=channel, start_time=start_time, end_time=end_time, filename=filename, status=Clip.STATUS.done)

        return clip



class Thumb(models.Model):
    """
    Model to reference video thumbnail
    """
    channel = models.ForeignKey(Channel)
    datetime = models.DateTimeField(null=False)
    filename = models.FileField()

    def __unicode__(self):
        return 'Thumb {} {}'.format(self.channel.name,
                                    self.datetime.strftime('%d/%m/%Y %H:%M:%S'))


