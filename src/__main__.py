import os
import sys
import argparse

import manifest
import compiler

def init_wrapper(args):
	"""init projct wrapper"""
	try:
		man = manifest._get_manifest(args.project_path)
	except IOError:
		pass
	else:
		ans = raw_input("py2so.json already exists. Re-init? [Y/n] ")
		if ans != "Y":
			sys.exit()

	try:
		manifest.init(project_path=args.project_path,
					  build_dir=args.build_dir,
					  compiled_dir=args.compiled_dir)
	except IOError, e:
		print repr(e)
	else:
		print "py2so project init at {0}".format(args.project_path)

def add_wrapper(args):
	"""add file to project wrapper"""
	try:
		manifest.add_file(args.file_path, args.project_path)
	except Exception, e:
		print repr(e)
	else:
		print "added 1 file to manifest {0}".format(args.project_path)

def remove_wrapper(args):
	"""remove file from project wrapper"""
	try:
		manifest.remove_file(args.file_path, args.project_path)
	except Exception, e:
		print repr(e)
	else:
		print "removed 1 file from {0}".format(args.project_path)

def destroy_wrapper(args):
	"""destroy project wrapper"""
	try:
		manifest.destroy(args.project_path)
	except Exception, e:
		print repr(e)
	else:
		print "py2so project destroyed at {0}".format(args.project_path)

def list_wrapper(args):
	"""list files in manifest wrapper"""
	try:
		for f, c in manifest.get_files(args.project_path).iteritems():
			print f, ":", c
	except Exception, e:
		print repr(e)

def set_wrapper(args):
	"""set key,value in manifest wrapper"""
	try:
		manifest.set_key(args.key, args.value, args.project_path)
	except Exception, e:
		print repr(e)
	else:
		print "'{0}' (key) set to '{1}' (value) in manifest".format(args.key, args.value)

def compile_wrapper(args):
	"""compile the project wrapper"""
	try:
		compiles, skips = compiler._get_files_to_compile(args.project_path)

		for f in compiles:
			print "compile:", os.path.basename(f), "->",
			print os.path.basename(compiler._get_so_path_from_py_path(f))

		for f in skips:
			print "skip:", os.path.basename(f), "->",
			print os.path.basename(compiler._get_so_path_from_py_path(f)), "(up-to-date)"

		if not args.display_only:
			compiler.port_and_compile(args.project_path,
									  compiles=compiles,
									  keep_cython=args.keep_cython)
	except Exception, e:
		print repr(e)

def get_args():

	parser = argparse.ArgumentParser()

	parser.add_argument("-p", "--project_path", default=os.getcwd())

	subparsers = parser.add_subparsers()

	# manifest : init
	init_opts = subparsers.add_parser("init")
	#init_opts.add_argument("-p", "--project_path", default=os.getcwd())
	init_opts.add_argument("-b", "--build_dir")
	init_opts.add_argument("-c", "--compiled_dir")
	init_opts.set_defaults(func=init_wrapper)

	# manifest : add file
	add_opts = subparsers.add_parser("add")
	#add_opts.add_argument("-p", "--project_path", default=os.getcwd())
	add_opts.add_argument("file_path")
	add_opts.set_defaults(func=add_wrapper)

	# manifest: remove file
	rem_opts = subparsers.add_parser("remove")
	#rem_opts.add_argument("-p", "--project_path", default=os.getcwd())
	rem_opts.add_argument("file_path")
	rem_opts.set_defaults(func=remove_wrapper)

	# manifest: destroy
	des_opts = subparsers.add_parser("destroy")
	#des_opts.add_argument("-p", "--project_path", default=os.getcwd())
	des_opts.set_defaults(func=destroy_wrapper)

	# manifest: list
	lis_opts = subparsers.add_parser("list")
	#lis_opts.add_argument("-p", "--project_path", default=os.getcwd())
	lis_opts.set_defaults(func=list_wrapper)

	# manifest: set
	set_opts = subparsers.add_parser("set")
	#set_opts.add_argument("-p", "--project_path", default=os.getcwd())
	set_opts.add_argument("key")
	set_opts.add_argument("value")
	set_opts.set_defaults(func=set_wrapper)


	# compiler: compile
	com_opts = subparsers.add_parser("compile")
	#com_opts.add_argument("-p", "--project_path", default=os.getcwd())
	com_opts.add_argument("--display_only", action="store_true", default=False)
	com_opts.add_argument("--keep_cython", action="store_true", default=False)
	com_opts.set_defaults(func=compile_wrapper)

	return parser.parse_args()


def main():
	"""
	Module CMD entry point!
	"""
	args = get_args()
	args.project_path = os.path.abspath(args.project_path)
	args.func(args)

if __name__ == "__main__":
	# direct package call
	main()
