import os, time

class DirWatcher:
	def __init__(self, dirPath):
		self.dirPath=dirPath
		self.before = dict ([(f, None) for f in os.listdir (self.dirPath)])
	def getChanges:
  		after = dict ([(f, None) for f in os.listdir (self.dirPath)])
		added = [f for f in after if not f in before]
  		removed = [f for f in before if not f in after]
  		if added: print "Added: ", ", ".join (added)
		if removed: print "Removed: ", ", ".join (removed)
  		self.before = after
		return (added, removed)q

