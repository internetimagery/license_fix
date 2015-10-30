#!/usr/bin/env python
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

    def message(s, *text):
        def write():
            print ", ".joint(text)
        utils.executeDeferred(write)

    def wait(s):
        try:
            cmds.scriptJob(
                ro=True,
                ie=lambda: s.fixfile(cmds.file(q=True, sn=True)))
                # ie = lambda: threading.Thread(
                #     target=s.fixfile,
                #     args=(cmds.file(q=True, sn=True),),
                #     daemon=True).start())
        except:
            s.message(traceback.format_exc())

    def fixfile(s, filename):
        ext = os.path.splitext(filename)[1]
        filename = os.path.realpath(filename)
        reg = ""
        if ext == ".ma":
            reg = r"fileInfo\s*?([\"'])license(?<!\\)\1\s*?([\"'])(?P<val>\w+?)(?<!\\)\2"
        # if ext == ".mb":
        #     reg = r"license.+?(?P<val>\w+)"
        if reg and os.path.isfile(filename):
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

import maya.utils as utils
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
