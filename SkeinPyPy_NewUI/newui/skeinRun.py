from __future__ import absolute_import

import platform, os, subprocess, sys

from skeinforge_application.skeinforge_utilities import skeinforge_craft

def getPyPyExe():
	"Return the path to the pypy executable if we can find it. Else return False"
	if platform.system() == "Windows":
		exeName = "pypy.exe"
		pypyExe = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../pypy/pypy.exe"));
	else:
		exeName = "pypy"
		pypyExe = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../pypy/bin/pypy"));
	if os.path.exists(pypyExe):
		return pypyExe

	path = os.environ['PATH']
	paths = path.split(os.pathsep)
	for p in paths:
		pypyExe = os.path.join(p, exeName)
		if os.path.exists(pypyExe):
			return pypyExe 
	return False

def runSkein(fileNames):
	"Run the slicer on the files. If we are running with PyPy then just do the slicing action. If we are running as Python, try to find pypy."
	pypyExe = getPyPyExe()
	for fileName in fileNames:
		if platform.python_implementation() == "PyPy":
			skeinforge_craft.writeOutput(fileName)
		elif pypyExe == False:
			print "************************************************"
			print "* Failed to find pypy, so slicing with python! *"
			print "************************************************"
			skeinforge_craft.writeOutput(fileName)
			print "************************************************"
			print "* Failed to find pypy, so sliced with python!  *"
			print "************************************************"
		else:
			subprocess.call([pypyExe, os.path.join(sys.path[0], sys.argv[0]), fileName])

def getSkeinCommand(filename):
	pypyExe = getPyPyExe()
	if pypyExe == False:
		pypyExe = sys.executable
	return [pypyExe, os.path.join(sys.path[0], os.path.split(sys.argv[0])[1]), filename]
