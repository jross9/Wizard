#!/usr/bin/python3

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Glb as G

# ---------------------------------------------------------------------
def List2Str(lst):
	# ---------------------------------------------
	return '\n'.join(lst) + '\n'

# ---------------------------------------------------------------------
def List2StrSrc(src, lst):
	# ---------------------------------------------
	if (src.UNIX):
		return '\n'.join(lst)
	else:
		return '\r\n'.join(lst)
