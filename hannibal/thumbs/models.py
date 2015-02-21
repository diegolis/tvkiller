from django.db import models
from django.conf import settings
import os

# Create your models here.
class Channel(models.Model):
    """
    Model to represent TV Channel

    device_name & device_slot reference recording technologies
    """

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
        """Return base dir for storing this channel's thumbs"""
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
    """a chunk of video captured from a channel.
    It's the source for clips"""
    pass


class Clip(BaseVideo):
    """a videoclip generated cutting/concatenating
    origin videos"""
    pass

    @classmethod
    def create_from_channel(channel, start_time, end_time):
        """
        create (if needed) a clip instance for the channel and time segment given
        """
        pass


class Thumb(models.Model):
    """
    Model to reference video thumbnail
    """
    channel = models.ForeignKey(Channel)
    datetime = models.DateTimeField(null=False)

    def filepath(self):
        """Return file path where this thumb should live."""
        # return value example:
        # '/thumbs/1/20150215/1600/012.jpg'

        basedirs = self.datetime.strftime('%Y%m%d_%H%M').split('_')
        # append thumb name
        basedirs.append('{:03d}'.format(self.datetime.second))
        fp = os.path.join(self.channel.base_dir(), *basedirs)
        return fp

    def exists(self):
        return os.path.exists(self.filepath())

    def __str__(self):
        return 'Thumb {} {}'.format(self.channel.name,
                                    self.datetime.strftime('%d/%m/%Y %H:%M:%S'))


