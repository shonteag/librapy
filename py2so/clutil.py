"""
Command line utilities for py2so package.
"""
from __future__ import absolute_import

from pathlib import Path
import json
import os

from . import project



def _is_project_root(path):
	"""
	check for a manifest file at path
	"""
	path = Path(path, project.MANIFEST_NAME)
	return path.is_file()

def _find_root():
	"""
	step up the CWD until we find a manifest file
	"""
	cwd = Path(os.getcwd())
	while not _is_project_root(cwd):
		cwd = Path("".join(cwd.parts[:-1]))
	return cwd

def init(args):
	"""
	handles positional argument "init"
	"""
	manifest_path = Path(os.getcwd(), project.MANIFEST_NAME)

	if manifest_path.exists() and manifest_path.is_file():
		overwrite = str(raw_input(
			"py2so has detected a project at this root.\noverwrite? (y/n) "))
		if overwrite != "y":
			return

	d = {
		"profiles": {
			"linux2": {
	            "portext": "c",
	            "compiledir": "compile/linux",
	            "compilecmd": "gcc -shared -pthread -fPIC -fwrapv -O2 -Wall"\
	            			  " -fno-strict-aliasing -I/usr/include/python2.7"\
	            			  " -o {compilepath} {portpath}",
	            "compileext": "so",
	            "portdir": "build/linux",
	            "portcmd": "cython {file} -o {portpath}"
			},
			"windows": {
	            "portext": "c", 
	            "compiledir": "compile/windows", 
	            "compilecmd": "cl /LD /IC:/python/include/python27 {portpath}"\
	            			  " /F{compilepath}", 
	            "compileext": "dll", 
	            "portdir": "build/windows", 
	            "portcmd": "cython {file} -o {portpath}"	
			}
		},
		"manifest": {}
	}

	with open(str(manifest_path), 'w') as f:
		json.dump(d, f, ensure_ascii=True, indent=4)

	print "project initialized"

def add(args):
	"""
	add a file to the project
	"""
	root = _find_root()

	# we need the relative path to insert into manifest
	filepath = Path(args.filepath)
	relativepath = filepath.relative_to(root)

	# get the project
	p = project.Project(root)
	p.add(relative_path)
	print "{0} added to manifest at {1}".format(filepath.parts[-1], str(root))

def remove(args):
	"""
	remove a file from the project manifest
	"""
	root = _find_root()

	filepath = Path(args.filepath)
	relativepath = filepath.relative_to(root)

	p = project.Project(root)
	p.remove(relative_path)
	print "{0} removed from manifest at {1}".format(filepath.parts[-1], str(root))

def build(args):
	"""
	compile the project
	"""
	root = _find_root()
	p = project.Project(root)
	compiled, skipped = p.build(args.profile)

	print " compiled\n".join(x for x in compiled)
