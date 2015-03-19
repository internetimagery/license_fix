import maya.cmds as cmds
import sys, re, shutil

def fix_file(file):
	r = open( file, "r")
	w = open( "%s.tmp" %file, "w")
	reg = re.compile("(fileInfo.+license.+\")(\w+)(\".*)")
	for line in r.readlines():
		w.write( reg.sub("\\1education\\3", line) )
	r.close()
	w.close()
	shutil.move( "%s.tmp" %file, file)
	print "License changed to \"education\" in file: %s" %file

def get_file():
	f = cmds.file(q=True,list=True)[0]
	if f.endswith(".ma"):
		fix_file(f)

process = cmds.scriptJob(e=['SceneSaved',get_file])
print "Watching for saves in process %s" %process
