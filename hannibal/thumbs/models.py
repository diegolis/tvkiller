from django.db import models
from django.db.models import Q
from django.conf import settings
import os
from django.db.models import permalink
from datetime import timedelta
from django.utils.text import slugify
from moviepy.editor import VideoFileClip, concatenate_videoclips
from model_utils.fields import StatusField
from model_utils import Choices
from hashids import Hashids

from thumbs.tasks import create_videoclip


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
        if not self.end_time:
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

        self.hashid = hashids.encode(*map(ord, str(self.filename)))[0:20]
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
                                             Q(start_time__lte=start_time, end_time__gte=end_time)).values_list('id', flat=True))

        if not sources:
            return None
        filename = '%s_%s_%s.webm' % (slugify(channel.name), start_time.strftime("%Y%m%d%H%M%S"),
                                      end_time.strftime("%Y%m%d%H%M%S"))

        clip = Clip.objects.create(channel=channel, start_time=start_time, end_time=end_time, filename=filename, status=Clip.STATUS.in_process)

        create_videoclip.delay(clip.id, sources, start_time.strftime('%Y-%m-%dT%H:%M:%S%Z'), end_time.strftime('%Y-%m-%dT%H:%M:%S%Z'), filename)
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


