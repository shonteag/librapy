import os
import sys
import argparse

import manage


def init_wrapper(args):
	"""init projct wrapper"""
	manage.init(project_path=args.project_path)

def add_wrapper(args):
	"""add file to project wrapper"""
	manage.add_file(args.file_path, args.project_path)

def remove_wrapper(args):
	"""remove file from project wrapper"""
	manage.remove_file(args.file_path, args.project_path)

def destroy_wrapper(args):
	"""destroy project wrapper"""
	manage.destroy(args.project_path)


def get_args():

	parser = argparse.ArgumentParser()

	subparsers = parser.add_subparsers()

	# MANAGE : init
	init_opts = subparsers.add_parser("init")
	init_opts.add_argument("-p", "--project_path", default=os.getcwd())
	init_opts.set_defaults(func=init_wrapper)

	# MANAGE : add file
	add_opts = subparsers.add_parser("add")
	add_opts.add_argument("-p", "--project_path", default=os.getcwd())
	add_opts.add_argument("file_path")
	add_opts.set_defaults(func=add_wrapper)

	# MANAGE: remove file
	rem_opts = subparsers.add_parser("remove")
	rem_opts.add_argument("-p", "--project_path", default=os.getcwd())
	rem_opts.add_argument("file_path")
	rem_opts.set_defaults(func=remove_wrapper)

	# MANAGE: destroy
	des_opts = subparsers.add_parser("destroy")
	des_opts.add_argument("-p", "--project_path", default=os.getcwd())
	des_opts.set_defaults(func=destroy_wrapper)

	return parser.parse_args()


if __name__ == "__main__":
	# direct package call
	args = get_args()
	args.func(args)