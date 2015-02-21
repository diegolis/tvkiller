# -*- coding: utf8 -*-

from __future__ import print_function

from inotify import watcher
import inotify
import sys
import traceback
import os
import re
import subprocess
import local_settings


def generate_thumbnails(srcpath, dstpath, ffmpeg_bin):
    # srcpath = '/aaaaa/bbbb/cccc/ddd/eeeeeee_ffffffff_gggg.avi'
    # dstpath = '/zzzz/xxxx/yyyyy/'
    # ffmpeg_bin = '/usr/bin/ffmpeg'

    file_name = srcpath[srcpath.rindex('/')+1:-4]
    #file_path = srcpath[:srcpath.rindex('/')+1]
    
    searchObj = re.search(r'(.*)_(.*)_(.*)_(.*)', file_name, re.M|re.I)
    fdate = searchObj.group(3)
    ftime = searchObj.group(4)
    
    file_datetime = datetime.datetime(fdate[:4], fdate[4:6], fdate[6:], ftime[:2], ftime[2:4])

    finalpath = os.path.join(dstpath, fdate, ftime[:-2])

    try:
        os.makedirs(finalpath)
    except:
        pass    # probably folders exists.
    
    cmd = "%s -i %s -f image2 -vf fps=fps=1 %s"
    cmd = cmd % (ffmpeg_bin, srcpath, finalpath + '%03d.jpg')
    os.system(cmd)

    ###
    # Here database query.
    ###


def main(source, storage, ffmpeg_bin=None):

    w = watcher.AutoWatcher()

    try:
        w.add_all(source, inotify.IN_CLOSE_WRITE)
    except OSError as err:
        print('%s: %s' % (err.filename, err.strerror), file=sys.stderr)

    # If we have nothing to watch, don't go into the read loop, or we'll
    # sit there forever.

    if not w.num_watches():
        print("no files to watch", file=sys.stderr)
        sys.exit(1)

    while w.num_watches():
        # The Watcher.read method returns a list of event objects.
        for evt in w.read():
            # The inotify.decode_mask function returns a list of the
            # names of the bits set in an event's mask.  This is very
            # handy for debugging.
            print(repr(evt.fullpath), ' | '.join(inotify.decode_mask(evt.mask)))

if __name__=="__main__":

    try:
        ffmpeg = local_settings.FFMPEG
    except:
        ffmpeg = 'ffmpeg' #try ffmpeg_bin installed

    try:
        main(local_settings.SOURCE, 
            local_settings.STORAGE,
            ffmpeg)
    except KeyboardInterrupt:
        print("Shutdown requested...exiting.")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
