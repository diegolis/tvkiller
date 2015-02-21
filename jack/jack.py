# -*- coding: utf8 -*-

import sys

def generate_thumbnails(srcpath, dstpath, channel):
    pass

def main(source, storage, ffmpeg_bin=None):
    pass

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
        print "Shutdown requested...exiting."
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)
