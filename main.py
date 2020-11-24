#!/usr/bin/env python

import sys
import time
import os
import shutil
import re
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def create_regexp(exts):
    trim_exts = list(map(lambda x: x[2:], exts))
    # print(trim_exts)
    return ".*\\.(" + "|".join(trim_exts) + ")"


def make_handler(exts, source, target):
    class DirectoryHandler(PatternMatchingEventHandler):

        # def on_modified(self, event):
        #     print("Modified")
        #     print(event)

        def on_created(self, event):
            files = os.listdir(source)
            # print(files)
            # print(create_regexp(exts))
            for i in range(len(files)):
                if(re.match(create_regexp(exts), files[i])):
                    shutil.move(os.path.join(source, files[i]), target)

    return DirectoryHandler(patterns=[*exts])


if __name__ == '__main__':
    args = sys.argv[1:]
    exts = list(map(lambda x: "*"+x, args[2:]))
    # print(args)
    # print(exts)
    observer = Observer()
    observer.schedule(make_handler(
        exts, args[0], args[1]), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

    # Use kill %jobID to terminate
