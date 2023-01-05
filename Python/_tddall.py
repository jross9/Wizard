#!/usr/bin/python3

import unittest

import Glb as G
import Dbg

# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	G.LogCount('TDD_All', 'Unit (Python)')
	# -----------------------------------------------------------------
	Dbg.LogOff = True
	# -----------------------------------------------------------------
	testsuite = unittest.TestLoader().discover('TDD', pattern='tdd*.py')
	unittest.TextTestRunner(verbosity=1).run(testsuite)
