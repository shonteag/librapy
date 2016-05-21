import os
import sys
import argparse

import manifest


def init_wrapper(args):
	"""init projct wrapper"""
	manifest.init(project_path=args.project_path,
				  build_dir=args.build_dir,
				  compiled_dir=args.compiled_dir)

def add_wrapper(args):
	"""add file to project wrapper"""
	manifest.add_file(args.file_path, args.project_path)

def remove_wrapper(args):
	"""remove file from project wrapper"""
	manifest.remove_file(args.file_path, args.project_path)

def destroy_wrapper(args):
	"""destroy project wrapper"""
	manifest.destroy(args.project_path)

def list_wrapper(args):
	"""list files in manifest wrapper"""
	for f, c in manifest.get_files(args.project_path).iteritems():
		print f, ":", c


def get_args():

	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	# manifest : init
	init_opts = subparsers.add_parser("init")
	init_opts.add_argument("-p", "--project_path", default=os.getcwd())
	init_opts.add_argument("-b", "--build_dir")
	init_opts.add_argument("-c", "--compiled_dir")
	init_opts.set_defaults(func=init_wrapper)

	# manifest : add file
	add_opts = subparsers.add_parser("add")
	add_opts.add_argument("-p", "--project_path", default=os.getcwd())
	add_opts.add_argument("file_path")
	add_opts.set_defaults(func=add_wrapper)

	# manifest: remove file
	rem_opts = subparsers.add_parser("remove")
	rem_opts.add_argument("-p", "--project_path", default=os.getcwd())
	rem_opts.add_argument("file_path")
	rem_opts.set_defaults(func=remove_wrapper)

	# manifest: destroy
	des_opts = subparsers.add_parser("destroy")
	des_opts.add_argument("-p", "--project_path", default=os.getcwd())
	des_opts.set_defaults(func=destroy_wrapper)

	# manifest: list
	lis_opts = subparsers.add_parser("list")
	lis_opts.add_argument("-p", "--project_path", default=os.getcwd())
	lis_opts.set_defaults(func=list_wrapper)

	return parser.parse_args()


def main():
	"""
	Module CMD entry point!
	"""
	args = get_args()
	args.func(args)

if __name__ == "__main__":
	# direct package call
	main()
