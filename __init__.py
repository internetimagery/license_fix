import maya.cmds as cmds
import fileinput
import os
import re


def validateFile():
    """
    Check file exists.
    """
    f = cmds.file(q=True, sn=True)
    return f if os.path.isfile(f) and f.endswith(".ma") else False


def licenseChange(license):
    """
    Find, replace license with provided name
    """
    f = validateFile()
    if f:
        reg = "^[ \t]*fileInfo"  # file info tag
        reg += "[ \t]+(\"|')license\\1"  # License section
        reg += "[ \t]+(\"|')\w+\\2"
        exp = re.compile(reg)
        match = None
        for line in fileinput.input(f, inplace=True):
            if match:
                print line,
            else:
                match = exp.match(line)  # Search for section to replace
                if match:
                    print "fileInfo \"license\" \"%s\"\n" % license,
                else:
                    print line,
        print "License changed to %s in file: %s\n" % (license, f),


def activate(license):
    """
    Turn on automatic fixing
    """
    process = cmds.scriptJob(e=['SceneSaved', lambda: licenseChange(license)])
    print "Watching for saves in process %s" % process
