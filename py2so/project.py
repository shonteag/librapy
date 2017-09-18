"""
Utilities for creating and managing py2so projects.
"""
from __future__ import absolute_import

import os
import hashlib
import json
import functools
from pathlib import Path

from . import profile



MANIFEST_NAME = ".manifest.py2so"

class Project(object):
	"""
	Represents a py2so project, tracking file updates and 

	:param str root: the root of the project (where '.manifest.py2so' is
		located). it should be an absolute path!
	"""
	def __init__(self, root):
		self.root = Path(root)
		self.manifest_path = Path(root, MANIFEST_NAME)
		self.manifest = {}
		self.profiles = {}

		with open(str(self.manifest_path), 'rw') as f:
			d = f.read()
			if not d:
				pass
			else:
				temp = json.loads(d)
				self.manifest = temp["manifest"]
				self.profiles = temp["profiles"]

	def update_manifest(self):
		"""
		write to the manifest file the updated details
		"""
		d = {
			"manifest": self.manifest,
			"profiles": self.profiles
		}
		with open(str(self.manifest_path), 'w') as f:
			json.dump(d, f, ensure_ascii=True, indent=4)

	def update_after(function):
		"""
		decorator to write manifest update to file
		"""
		functools.wraps(function)
		def wrapper(self, *args, **kwargs):
			ret = function(self, *args, **kwargs)
			self.update_manifest()
			return ret
		return wrapper

	def get_manifest(self):
		"""
		return a dict of files in the project
		"""
		return self.manifest

	@update_after
	def add(self, path):
		"""
		add a path to the manifest

		:param str path: the path to add, can be path to file or folder,
			but it must always be RELATIVE to the root
		:raises IOError: if path does not exist
		"""
		path = Path(path)
		fullpath = Path(self.root, path)
		try:
			relativepath = path.relative_to(self.root)
		except ValueError, e:
			# ``path`` is already relative
			relativepath = path

		if fullpath.is_file():
			h = hashlib.md5()
			h.update(open(str(fullpath)).read())
			checksum = h.hexdigest()

			self.manifest[str(relativepath)] = [checksum, ]

		elif fullpath.is_dir():
			for dirpath, dirnames, filenames in os.walk(str(fullpath)):
				for f in filenames + dirnames:
					_path = Path(dirpath, f)
					self.add(_path)

		else:
			raise IOError("{0} does not exist".format(path))

	@update_after
	def remove(self, path):
		"""
		remove a path from the manifest
		"""
		path = Path(path)
		fullpath = Path(self.root, path)
		try:
			relativepath = path.relative_to(self.root)
		except ValueError, e:
			# ``path`` is already relative
			relativepath = path

		if str(path) not in self.manifest:
			# don't give up yet, it might be a directory name
			for entry in self.manifest.keys():
				entry = Path(entry)
				try:
					entry.relative_to(path)
				except ValueError, e:
					pass
				else:
					self.manifest.pop(str(entry))

		else:
			self.manifest.pop(str(relativepath))

	@update_after
	def add_profile(self,
					name,
					portdir,
					compiledir,
					portcmd,
					compilecmd,
					portext,
					compileext):
		"""
		add a port-compile profile to the project. it can be configured
		and called later during port/compile time.
		"""
		self.profiles[name] = {
			"portdir": portdir,
			"compiledir": compiledir,
			"portcmd": portcmd,
			"compilecmd": compilecmd,
			"portext": portext,
			"compileext": compileext
		}

	@update_after
	def remove_profile(self, name):
		"""
		remove a profile from the project
		"""
		self.profiles.pop(name)

	def get_profile(self, name):
		"""
		get a profile object
		"""
		return profile.IProfile(name, self.root, **self.profiles[name])

	def build(self, profile_name):
		"""
		port all files on the manifest
		"""
		ported = []
		skipped = []

		p = self.get_profile(profile_name)
		for filepath, (checksum) in self.manifest.items():
			path = Path(filepath)
			fullpath = Path(self.root, path)
			if not fullpath.is_file():
				raise IOError("{0} file is not an existing file".format(
					path))

			with open(str(fullpath)) as f:
				c = hashlib.md5()
				c.update(f.read())
				cs = c.hexdigest()

			if cs != checksum or not p.get_compile_outpath(path).exists():
				# if the file has been updated
				p.port(path)
				p.compile(path)
				ported.append(str(path))
				# update the hash value
				self.add(str(path))
			else:
				skipped.append(path)

		return ported, skipped

