"""
compile.py

A module dedicated to the compiling of
librapy projects.
.py -> .c -> .o -> .so
|---------||---------|
  Cython       gcc
"""

import os
import sys
import subprocess

import manifest