from django.core.management.base import BaseCommand, CommandError
from thumbs.models import Thumb, Channel, Origin
from django.conf import settings

from inotify import watcher
import inotify
import os
import re
import datetime
import fcntl
import subprocess32
import threading

def add_thumb(channel, base_dtime, path):
    """ Process the path of a newly added thumb and add the corresponding objecto to the db. """
    offset, _, _ = os.path.basename(path).rpartition('.')
    dtime = base_dtime + datetime.timedelta(seconds=int(offset) - 1)
    Thumb.objects.create(channel=channel, datetime=dtime, filename=path)

class Command(BaseCommand):
    args = '<vid_file>'
    help = 'Generates thumbnails for video'

    def handle(self, *args, **options):
        # srcpath = '/aaaaa/bbbb/cccc/ddd/eeeeeee_ffffffff_gggg.avi'
        # ffmpeg_bin = '/usr/bin/ffmpeg'

        srcpath, ffmpeg_bin = args[:2]

        file_name = srcpath[srcpath.rindex('/')+1:-4]
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

        Origin.objects.create(channel=chan, start_time=file_dtime, filename=os.path.join(settings.SOURCE, file_name))
        finalpath = os.path.join(settings.THUMB_DIR, str(chan.id), fdate, ftime[:-2]) + "/"

        try:
            os.makedirs(finalpath)
        except:
            pass    # probably folders exists.

        # Use an anonymous pipe to pass data to ffmpeg, so that it blocks waiting for more file data
        pipe_read, pipe_write = os.pipe()

        w = watcher.Watcher()
        # Watch the video file for writes and close.
        source_wd = w.add(srcpath, inotify.IN_MODIFY | inotify.IN_CLOSE_WRITE)
        # Watch thumb dir for newly created thumbs.
        thumbs_wd = w.add(finalpath, inotify.IN_CLOSE_WRITE)

        # Call ffmpeg in other process with our pipe as source.
        ffmpeg_proc = subprocess32.Popen([ffmpeg_bin, '-i', "pipe:0", '-f', 'image2', '-s', '320x240', '-vf', 'fps=fps=1', os.path.join(finalpath, '%03d.jpg')], stdin=pipe_read)

        with open(srcpath, 'rb') as sourcef:

            # Set nonblocking reads
            orig_fl = fcntl.fcntl(sourcef, fcntl.F_GETFL)
            fcntl.fcntl(sourcef, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)
            
            threshold = watcher.Threshold(sourcef.fileno(), 1024)

            pipef = os.fdopen(pipe_write, 'wb')

            timer = None
            # Lock will let us call the "close_all" func below in another thread safely.
            lock = threading.Lock()

            # Store this separately so that we access w only inside the lock.
            nwatches = w.num_watches()
            while nwatches:
                with lock:
                    # The Watcher.read method returns a list of event objects.
                    for evt in w.read():
                        mask_list = inotify.decode_mask(evt.mask)
                        if evt.wd == source_wd and 'IN_MODIFY' in mask_list:
                            if threshold():
                                data = ''

                                while True:
                                    new_data = sourcef.read()
                                    if not new_data:
                                        break
                                    data += new_data

                                pipef.write(data)
                                
                        if evt.wd == source_wd and 'IN_OPEN' in mask_list:
                            if timer is not None:
                                timer.cancel()
                        if evt.wd == source_wd and 'IN_CLOSE_WRITE' in mask_list:
                            def close_all():
                                with lock:
                                    pipef.close()
                                    ffmpeg_proc.wait()
                                    w.remove(source_wd)
                                    w.remove(thumbs_wd)
                            timer = threading.Timer(60, close_all)
                        if evt.wd == thumbs_wd and 'IN_CLOSE_WRITE' in mask_list:
                            add_thumb(chan, file_dtime, evt.fullpath)
                    
                    nwatches = w.num_watches()
