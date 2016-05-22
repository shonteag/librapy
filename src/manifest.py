"""
manifest.py

Module for generating project manifests,
checking for file updates, etc.
"""

import os
import sys
import json
import hashlib


MANIFEST_FILE_NAME = "py2so.json"


def _make_lib_path(path):
	"""
	Path within the py2so module itself.
	"""
	base = os.path.dirname(os.path.abspath(__file__))
	return os.path.join(base, path)

def _make_project_path(path, project_path):
	"""
	Path within the intended project directory.
	"""
	base = os.path.abspath(project_path)
	return os.path.join(base, path)

def _make_key_path(path, project_path):
	"""
	Shorten project path to relative path.
	"""
	return path.replace(project_path + os.sep, "")

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
	in the py2so package.
	"""
	return json.load(open(
		_make_lib_path(os.path.join("template", "manifest.json"))))

def _add_file(manifest, path, project_path):
	"""
	add a file and it's initial md5 sum
	to the py2so.json manifest file
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

def _update_file(manifest, path, project_path):
	"""
	update a files md5 checksum
	"""
	path = _make_key_path(path, project_path)
	if path not in manifest["files"]:
		raise KeyError("file {0} not in manifest".format(path))
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

def _get_files(manifest, project_path, full_path=False):
	"""
	return a dict of the filepaths, with md5 values
	"""
	files = {}
	for filepath, checksum in manifest["files"].iteritems():
		if full_path:
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


def update_file(path, project_path=None):
	"""
	Cmd entry to update a file md5 checksum.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)

	path = _make_key_path(path, project_path)
	manifest = _update_file(manifest, path, project_path)
	_write_manifest(manifest, project_path)


def get_files(project_path=None, full_path=False):
	"""
	Cmd entry to retrieve dict of files and
	checksums in manifest.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)
	return _get_files(manifest, project_path, full_path=full_path)


def get_build_dir(project_path=None, full_path=False):
	"""
	Get the project's specified build directory.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)
	ret = manifest["build_dir"]
	if full_path:
		ret = _make_project_path(ret, project_path)
	return ret

def get_compiled_dir(project_path=None, full_path=False):
	"""
	Get the project's specified compiled directory.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)
	ret = manifest["compiled_dir"]
	if full_path:
		ret = _make_project_path(ret, project_path)
	return ret

def set_key(key, value, project_path=None):
	"""
	Set a key in the manifest dict.
	"""

	project_path = _parse_project_path(project_path)
	manifest = _get_manifest(project_path)

	if key not in manifest:
		raise KeyError("key '{0}' not found in manifest".format(key))

	manifest[key] = value
	_write_manifest(manifest, project_path)