#!/usr/bin/env python
import maya.utils as utils
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
    def __init__(s, license):
        s.license = license
        s.listener = cmds.scriptJob(e=['SceneSaved', s.wait], ro=True)
        print "Watching for saves in process %s" % s.listener

    def message(s, text):
        def write():
            print text
        utils.executeDeferred(write)

    def wait(s):
        cmds.scriptJob(
            ro=True,
            ie=lambda: threading.Thread(
                target=s.fixfile,
                args=(cmds.file(q=True, sn=True),),
                daemon=True).start())

    def fixfile(s, filename):
        ext = os.path.splitext(filename)[1]
        filename = os.path.realpath(filename)
        reg = ""
        if ext == ".ma":
            reg = "fileInfo\\s+"  # File tag
            reg += "([\"'])(?P<key>.*?)(?<!\\\\)\\1\\s+"
            reg += "([\"'])(?P<val>.*?)(?<!\\\\)\\3"
        if ext == ".mb":
            reg = "license.+?(\\w+)"
        if reg and os.path.isfile(filename):
            search = True
            try:
                with tempfile.NamedTemporaryFile() as w:
                    with open(filename, "rb") as r:
                        for line in r:
                            if search:
                                match = re.search(reg, line)
                                if match:
                                    end = match.end()
                                    start = end - len(match.group(1))
                                    line = line[: start] + s.license + line[end :]
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

import maya.cmds as cmds
Fix("education")
# if __name__ == "__main__":
#     import argparse
#     parser = argparse.ArgumentParser(
#         description="Change license of maya file.")
#     parser.add_argument("license", help="License name.", type=str)
#     parser.add_argument("input", help="File for processing.", type=str)
#     args = parser.parse_args()
#     licenseChange(args.license, args.input)
# else:
#     import maya.cmds as cmds
