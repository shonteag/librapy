"""
compiler.py

A module dedicated to the compiling of
librapy projects.
.py -> .c -> .so
|---------||---|
  Cython    gcc
"""

import os
import sys
import subprocess
import hashlib

import manifest

def _get_c_path_from_py_path(pypath):
	return pypath.replace(".py", ".c")

def _get_so_path_from_py_path(pypath):
	return pypath.replace(".py", ".so")


def _get_files_to_compile(project_path):
	"""
	build a list of files to compile.
	check for existing .so and checksums
	of source .py files.
	"""

	compiles = []
	skips = []

	for f, c in manifest.get_files(project_path, True).iteritems():

		if not os.path.isfile(f):
			# file has since been deleted
			print project_path, f
			manifest.remove_file(manifest._make_key_path(f, project_path), project_path)
			continue

		h = hashlib.md5()
		h.update(open(f).read())
		h = h.hexdigest()

		if h != c:
			compiles.append(f)
		elif not os.path.isfile(_get_so_path_from_py_path(f)):
			compiles.append(f)
		else:  # h == c and os.path.isfile(_get_so_path_from_py_path(f))
			skips.append(f)

	return compiles, skips

def port_and_compile(project_path, compiles=None, keep_cython=False):
	"""
	cythonize and gcc to SO artifact.
	"""
	# run unitests TODO

	if compiles is None:
		compiles, skips = _get_files_to_compile(project_path)

	for f in compiles:
		# cythonize
		subprocess.call(["cython", "{0}".format(f), "-o", "{0}".format(_get_c_path_from_py_path(f))])
		# compile to SO
		subprocess.call(["gcc", "-shared", "-pthread", "-fPIC", "-fwrapv", "-O2", "-Wall", "-fno-strict-aliasing",
						 "-I/usr/include/python2.7", "-o", "{0}".format(_get_so_path_from_py_path(f)),
						 "{0}".format(_get_c_path_from_py_path(f))])
		if not keep_cython:
			os.remove(_get_c_path_from_py_path(f))
		manifest.update_file(f, project_path)
