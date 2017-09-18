"""
Provides an abstracted version of a port-compile profile.
"""

import subprocess
import os
from pathlib import Path



class IProfile(object):

	def __init__(self,
				 name,
				 root,
				 portdir=None,
				 compiledir=None,
				 portcmd=None,
				 compilecmd=None,
				 portext="c",
				 compileext="so"):
		self.name = name
		self.root = Path(root)

		# directories
		self.portdir = Path(portdir)
		self.compiledir = Path(compiledir)

		# commands
		self.portcmd = portcmd
		self.compilecmd = compilecmd

		# extensions
		self.portext = portext
		self.compileext = compileext

	@classmethod
	def load(cls, name, root, config):
		"""
		load from a dict

		:param str name: the name of this profile
		:param dict config: the configuration values for this profile
		"""
		return cls(name, root, **config)

	def get_port_outfile(self, path):
		return os.path.splitext(path.parts[-1])[0]+"."+self.portext
	def get_port_outfolder(self, path):
		return Path(self.portdir, "".join(path.parts[:-1]))
	def get_port_outpath(self, path):
		return Path(
			self.portdir,
			"".join(path.parts[:-1]),
			self.get_port_outfile(path))

	def get_compile_outfile(self, path):
		return os.path.splitext(path.parts[-1])[0]+"."+self.compileext
	def get_compile_outfolder(self, path):
		return Path(self.compiledir, "".join(path.parts[:-1]))
	def get_compile_outpath(self, path):
		return Path(
			self.compiledir,
			"".join(path.parts[:-1]),
			self.get_compile_outfile(path))

	def port(self, path):
		"""
		port a .py file to .c via the ``portcmd`` instance

		:param str path: the RELATIVE path to the file
		"""
		path = Path(path)

		inpath = Path(self.root, path)
		outfile = self.get_port_outfile(path)
		outfolder = self.get_port_outfolder(path)
		outpath = self.get_port_outpath(path)

		# check to make sure the folder exists
		if not outfolder.is_dir():
			os.makedirs(str(outfolder))

		cmd = self.portcmd.format(file=inpath, portpath=outpath)
		subprocess.call(cmd.split(" "))

	def compile(self, path):
		"""
		compile a .c to an output
		"""
		path = Path(path)

		inpath = self.get_port_outpath(path)
		outfile = self.get_compile_outfile(path)
		outfolder = self.get_compile_outfolder(path)
		outpath = self.get_compile_outpath(path)

		if not outfolder.is_dir():
			os.makedirs(str(outfolder))

		cmd = self.compilecmd.format(portpath=inpath, compilepath=outpath)
		subprocess.call(cmd.split(" "))

	def port_and_compile(self, path):
		"""
		perform full execution
		"""
		self.port(path)
		self.compile(path)
