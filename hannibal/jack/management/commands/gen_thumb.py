from django.core.management.base import BaseCommand, CommandError
from thumbs.models import Thumb, Channel, Origin
from django.conf import settings
import inotify
import os
import re
import datetime

class Command(BaseCommand):
    args = '<vid_file>'
    help = 'Add the new origin video and generates its thumbnails'

    def handle(self, *args, **options):
        # srcpath = '/aaaaa/bbbb/cccc/ddd/eeeeeee_ffffffff_gggg.avi'
        # ffmpeg_bin = '/usr/bin/ffmpeg'

        srcpath, ffmpeg_bin = args[:2]

        basename = os.path.basename(srcpath)
        file_name = os.path.splitext(basename)[0]

        #file_path = srcpath[:srcpath.rindex('/')+1]

        searchObj = re.search(r'(.*)_(.*)_(.*)_(.*)', file_name, re.M|re.I)
        fdevice = searchObj.group(1)
        fcamera = searchObj.group(2)
        fdate = searchObj.group(3)
        ftime = searchObj.group(4)

        # If channel doesn't exist, let the command die
        chan = Channel.objects.get(device_name=fdevice, device_slot=fcamera)

        file_dtime = datetime.datetime(int(fdate[:4]),
                                          int(fdate[4:6]),
                                          int(fdate[6:]),
                                          int(ftime[:2]),
                                          int(ftime[2:4]),
                                          int(ftime[4:]))
        Origin.objects.create(channel=chan, start_time=file_dtime, filename=os.path.join('sources', basename))

        finalpath = os.path.join(str(chan.id), fdate, ftime[:-2])
        try:
            os.makedirs(os.path.join(settings.MEDIA_ROOT, settings.THUMB_DIR, finalpath))
        except:
            pass    # probably folders exists.

        cmd = "%s -i %s -f image2 -vf fps=fps=1;scale=320:240 %s"
        cmd = cmd % (ffmpeg_bin, srcpath, os.path.join(settings.MEDIA_ROOT, settings.THUMB_DIR, finalpath, '%03d.jpg'))
        os.system(cmd)

        ###
        # Here database query.
        ###
        thumbs_data = []
        a_second = datetime.timedelta(seconds=1)

        for f in sorted(os.listdir(os.path.join(settings.MEDIA_ROOT, settings.THUMB_DIR, finalpath))):
            file_dtime += a_second
            thumbs_data.append((file_dtime , os.path.join(settings.THUMB_DIR, finalpath, f)))

        Thumb.objects.bulk_create(
                [Thumb(channel=chan, datetime=d, filename=f) for d, f in thumbs_data])


