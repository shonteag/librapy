"""
manifest.py

Module for generating project manifests,
checking for file updates, etc.
"""

import os
import sys
import json
import hashlib


MANIFEST_FILE_NAME = "librapy.json"


def _make_lib_path(path):
	"""
	Path within the librapy module itself.
	"""
	base = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(base, path)

def _make_project_path(path, project_path):
	"""
	Path within the intended project directory.
	"""
	base = os.path.abspath(project_path)
	return os.path.join(base, path)

def _parse_project_path(project_path):
	"""
	Parse the project_path.
	"""
	if project_path is None:
		project_path = os.getcwd()
	project_path = os.path.abspath(project_path)
	return project_path

def _get_manifest(project_path):
	"""
	Return the manifest dict at the project path,
	if none, return None.
	"""
	try:
		return json.load(
			open(_make_project_path(MANIFEST_FILE_NAME, project_path)))
	except IOError:
		raise IOError("no manifest file at {0}".format(project_path))

def _write_manifest(manifest, project_path):
	"""
	Write the passed manifest dict to the
	manifest at the project path.
	"""
	with open(_make_project_path(MANIFEST_FILE_NAME, project_path), "w") as manf:
		json.dump(manifest, manf, ensure_ascii=False,
				  indent=4, sort_keys=True)	

def _get_blank_manifest():
	"""
	Get a fresh manifest dict from the template
	in the librapy package.
	"""
	return json.load(open(
		_make_lib_path(os.path.join("template", "manifest.json"))))

def _add_file(manifest, path, project_path):
	"""
	add a file and it's initial md5 sum
	to the librapy.json manifest file
	"""
	if path in manifest["files"]:
		raise KeyError("file {0} already in manifest".format(path))
		return manifest

	try:
		h = hashlib.md5()
		h.update(open(_make_project_path(path, project_path)).read())
		manifest["files"][path] = h.hexdigest()
	except IOError:
		raise IOError("file {0} does not exist".format(path))
	return manifest

def _remove_file(manifest, path, project_path):
	"""
	remove a file from the projects manifest
	"""
	filepath = _make_project_path(path, project_path)
	if path in manifest["files"]:
		manifest["files"].pop(path)
	else:
		raise KeyError("file {0} not in manifest".format(path))
	return manifest

def _get_files(manifest, project_path):
	"""
	return a dict of the filepaths, with md5 values
	"""
	files = {}
	for filepath, checksum in manifest["files"].iteritems():
		filepath = _make_project_path(filepath, project_path)
		files[filepath] = checksum
	return files


def init(files=[],
		 project_path=None,
		 build_dir=None,
		 compiled_dir=None):
	"""
	Cmd entry to create a new project area.
	This is useful to avoid re-compilation of
	unchanged code.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_blank_manifest()

	if build_dir is not None:
		manifest["build_dir"] = build_dir
	if compiled_dir is not None:
		manifest["compiled_dir"] = compiled_dir

	for path in files:
		manifest = _add_file(manifest, path, project_path)

	# create the new manifest file in the project dir
	_write_manifest(manifest, project_path)


def destroy(project_path=None):
	"""
	Cmd entry point for destroying the project
	"""

	project_path = _parse_project_path(project_path)
	try:
		os.remove(_make_project_path(MANIFEST_FILE_NAME, project_path))
	except OSError:
		raise IOError("no manifest file at {0}".format(project_path))


def add_file(path, project_path=None):
	"""
	Cmd entry to add file to established manifest
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)

	manifest = _add_file(manifest, path, project_path)
	_write_manifest(manifest, project_path)


def remove_file(path, project_path=None):
	"""
	Cmd entry to remove file from established manifest
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)

	manifest = _remove_file(manifest, path, project_path)
	_write_manifest(manifest, project_path)


def get_files(project_path=None):
	"""
	Cmd entry to retrieve dict of files and
	checksums in manifest.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)
	return _get_files(manifest, project_path)


def get_build_dir(project_path=None):
	"""
	Get the project's specified build directory.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)
	return manifest["build_dir"]

def get_compiled_dir(project_path=None):
	"""
	Get the project's specified compiled directory.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)
	return manifest["compiled_dir"]