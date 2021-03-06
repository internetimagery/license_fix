#!/usr/bin/env python
try:
    import maya.cmds as cmds
    import maya.utils as utils
except ImportError:
    utils = None
import traceback
import threading
import tempfile
import os.path
import shutil
import re

class Fix(object):
    """
    Fix license in maya file
    """
    block = threading.Semaphore()
    def __init__(s, license):
        s.license = license

    def listen(s):
        def fire():
            th = threading.Thread(
                target=s.fixfile,
                args=(cmds.file(q=True, sn=True),)
            )
            th.daemon=True
            th.start()
        s.listener = cmds.scriptJob(e=[
            'SceneSaved',
            lambda: cmds.scriptJob(ie=fire, ro=True)
            ])
        print "Watching for saves in process %s" % s.listener

    def message(s, *text):
        def write():
            print ", ".join(text)
        utils.executeDeferred(write) if utils else write()

    def fixfile(s, filename):
        ext = os.path.splitext(filename)[1]
        filename = os.path.realpath(filename)
        reg = ""
        if ext == ".ma":
            reg = r"fileInfo\s*?([\"'])license(?<!\\)\1\s*?([\"'])(?P<val>\w+?)(?<!\\)\2"
        # if ext == ".mb":
        #     reg = r"license.+?(?P<val>\w+)"
        if reg and os.path.isfile(filename):
            with s.block:
                search = True
                try:
                    with tempfile.TemporaryFile() as w:
                        with open(filename, "rb") as r:
                            for line in r:
                                if search:
                                    match = re.search(reg, line)
                                    if match:
                                        pos = match.span("val")
                                        line = line[: pos[0]] + s.license + line[pos[1] :]
                                        search = False
                                w.write(line)
                        if not search:
                            w.seek(0)
                            with open(filename, "wb") as f:
                                for line in w:
                                    f.write(line)
                            s.message("License changed to \"%s\" in %s" % (s.license, filename))
                except:
                    s.message(traceback.format_exc())
