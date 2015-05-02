#!/usr/bin/env python
import fileinput
import os
import re


def validateFile(mayaFile):
    """
    Check file exists.
    """
    mayaFile = os.path.realpath(mayaFile)
    return mayaFile if os.path.isfile(mayaFile) and mayaFile.endswith(".ma") else False


def licenseChange(license, mayaFile):
    """
    Find, replace license with provided name
    """
    f = validateFile(mayaFile)
    if f:
        reg = "(fileInfo"  # file info tag
        reg += "[ \t]+(\"|')license\\2"  # License section
        reg += "[ \t]+(\"|'))(\w+)((?<!\\)\\3)"

        txt1 = "fileInfo[ \t]+"
        txt2 = "(\"|')license(?<!\\\\)\\2"
        txt3 = "(\"|').*?(?<!\\\\)\\3"
        reg = "(%s%s)[ \t]+%s" % (txt1, txt2, txt3)
        exp = re.compile(reg)
        match = None
        for line in fileinput.input(f, inplace=True):
            if match:
                print line,
            else:
                match = exp.match(line)
                if match:
                    print exp.sub("\\1 \\3%s\\3" % license, line),
                else:
                    print line,
        print "License changed to %s in file: %s\n" % (license, f),


def activate(license):
    """
    Turn on automatic fixing
    """
    process = cmds.scriptJob(e=['SceneSaved', lambda: licenseChange(license, cmds.file(q=True, sn=True))])
    print "Watching for saves in process %s" % process


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Change license of maya file.")
    parser.add_argument("license", help="License name.", type=str)
    parser.add_argument("input", help="File for processing.", type=str)
    args = parser.parse_args()
    licenseChange(args.license, args.input)
else:
    import maya.cmds as cmds
