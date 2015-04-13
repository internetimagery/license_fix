import resources

process = resources.cmds.scriptJob(e=['SceneSaved',resources.get_file])
print "Watching for saves in process %s" %process
