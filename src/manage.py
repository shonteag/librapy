"""
manage.py

Module for generating project manifests,
checking for file updates, etc.
"""

import os
import sys
import json
import hashlib


def _make_lib_path(path):
	base = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(base, path)

def _make_project_path(path, project_path):
	base = os.path.abspath(project_path)
	return os.path.join(base, path)

def _make_base_project_path(project_path):
	if project_path is None:
		project_path = os.getcwd()
	project_path = os.path.abspath(project_path)
	return project_path

def _get_manifest(project_path):
	try:
		return json.load(
			open(_make_project_path("librapy.json", project_path)))
	except IOError:
		return None

def _write_manifest(manifest, project_path):
	with open(_make_project_path("librapy.json", project_path), "w") as manf:
		json.dump(manifest, manf, ensure_ascii=False,
				  indent=4, sort_keys=True)	

def _get_blank_manifest():
	return json.load(open(
		_make_lib_path(os.path.join("template", "manifest.json"))))

def _add_file(manifest, path, project_path):
	"""
	add a file and it's initial md5 sum
	to the librapy.json manifest file
	"""
	if path in manifest["files"]:
		print "file already in manifest"
		return manifest

	try:
		h = hashlib.md5()
		h.update(open(_make_project_path(path, project_path)).read())
		manifest["files"][path] = h.hexdigest()
		print "added 1 file to {0}".format(project_path)
	except IOError:
		print "no file at path {0}".format(path)
	return manifest

def _remove_file(manifest, path, project_path):
	"""
	remove a file from the projects manifest
	"""
	filepath = _make_project_path(path, project_path)
	if path in manifest["files"]:
		manifest["files"].pop(path)
		print "removed 1 file from {0}".format(project_path)
	else:
		print "file not found in manifest {0}".format(project_path)
	return manifest


def init(files=[], project_path=None):
	"""
	Cmd entry to create a new project area.
	This is useful to avoid re-compilation of
	unchanged code.
	"""

	project_path = _make_base_project_path(project_path)
	print project_path

	manifest = _get_manifest(project_path)

	if manifest is not None:
		ans = raw_input("librapy.json already exists. Re-init? [Y/n] ")
		if ans != "Y":
			sys.exit()
	
	manifest = _get_blank_manifest()

	for path in files:
		manifest = _add_file(manifest, path, project_path)

	# create the new manifest file in the project dir
	_write_manifest(manifest, project_path)

	print "librapy project init with {0} source files".format(len(manifest["files"]))


def destroy(project_path=None):
	"""
	Cmd entry point for destroying the project
	"""

	project_path = _make_base_project_path(project_path)
	print project_path

	os.remove(_make_project_path("librapy.json", project_path))

	print "librapy project destroyed at {0}".format(project_path)


def add_file(path, project_path=None):
	"""
	Cmd entry to add file to established manifest
	"""

	project_path = _make_base_project_path(project_path)
	print project_path

	manifest = _get_manifest(project_path)

	if manifest is None:
		print "No manifest found at {0}. (Try using 'init' first)".format(project_path)
		sys.exit()

	manifest = _add_file(manifest, path, project_path)
	_write_manifest(manifest, project_path)


def remove_file(path, project_path=None):
	"""
	Cmd entry to remove file from established manifest
	"""

	project_path = _make_base_project_path(project_path)
	print project_path

	manifest = _get_manifest(project_path)

	if manifest is None:
		print "No manifest found at {0}. (Try using 'init' first)".format(project_path)
		sys.exit()

	manifest = _remove_file(manifest, path, project_path)
	_write_manifest(manifest, project_path)