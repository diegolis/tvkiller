from django.db import models
from django.conf import settings
import os

# Create your models here.
class Channel(models.Model):
    name = models.CharField(max_length=200, unique=True)
    device_name = models.CharField(max_length=200, default="")
    device_slot = models.CharField(max_length=200, default="")

    def save(self, *args, **kwargs):
        """ Create a directory for the thumbnails. """
        super(Channel, self).save(*args, **kwargs)
        try:
            os.mkdir(self.base_dir())
        except OSError:
            pass

    def __str__(self):
        return self.name

    def base_dir(self):
        return os.path.join(settings.THUMB_DIR, str(self.id))


class BaseVideo(models.Model):

    class Meta:
        abstract = True

    channel = models.ForeignKey(Channel)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)
    filename = models.CharField(max_length=200)

    def duration(self):
        """ Returns deltatime """
        return self.end_time - self.start_time


class Origin(BaseVideo):
    """a chunk of video captured from a channel. It's the source for clips"""
    pass


class Clip(BaseVideo):
    pass
    """a videoclip generated cutting/concatenating origin videos"""

    @classmethod
    def create_from_channel(channel, start_time, end_time):
        """
        create (if needed) a clip instance for the channel and time segment given
        """
        pass





