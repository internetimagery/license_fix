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

        reg = "fileInfo\\s+"  # File tag
        reg += "([\"'])license(?<!\\\\)\\1\\s+"
        reg += "([\"'])(?P<val>.*?)(?<!\\\\)\\2"
        exp = re.compile(reg)
        found = False
        for line in fileinput.input(f, inplace=True):
            if found:
                print line,
            else:
                match = exp.search(line)
                if match:
                    found = True
                    pos = match.span("val")
                    print line[:pos[0]] + license + line[pos[1]:],
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
