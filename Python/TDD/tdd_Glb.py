#
# Copyright James Ross (C) 2022
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
#!/usr/bin/python3

import unittest

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import tempfile

import Glb as G
import Dbg

# ---------------------------------------------------------------------
# just a sanity check ... 
# ---------------------------------------------------------------------
class Glb_Tests(unittest.TestCase):

	def test_Defaults(self):
		# -----------------------------------------
		self.assertEqual(G.WizDir, '..')
		self.assertEqual(G.WizLogPath, '../_countLog.txt')
		self.assertEqual(G.WizPyDir, '../Python')
		self.assertEqual(G.MkoDefRoot, '../Python/Templates')
		self.assertEqual(G.MkoTmpFolder, G.Temp + '/mako_modules')
		self.assertEqual(G.Temp, tempfile.gettempdir())

# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	G.LogCount('tdd_Glb', 'Unit (Python)')
	# -----------------------------------------------------------------
	Dbg.LogOff = True
	# -----------------------------------------------------------------
	unittest.main()
