"""
compile.py

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


