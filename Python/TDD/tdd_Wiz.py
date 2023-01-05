#
# Copyright James Ross (C) 2023
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
import unittest

import xml.etree.ElementTree as Et
import io
import uuid

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Glb as G
import Dbg
import TDD.UTLib as UT

import Wiz
import Xml

# ---------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------
class Node_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		node = Wiz.FSNode(sln)
		node.SetID('Node')
		# -----------------------------------------
		self.assertEqual(node.ID, 'Node')
		# -----------------------------------------
		self.assertEqual(node.IsFolder, False)
		# -----------------------------------------
		self.assertEqual(node.FolderPath, sln.FolderPath)
		# -----------------------------------------
		self.assertEqual(node.Folder, sln) 
		self.assertEqual(node.DefNamespace, 'Solution')

# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	G.LogCount('TDD', 'Unit (Python)')
	# -----------------------------------------------------------------
	Dbg.LogOff = True
	# -----------------------------------------------------------------
	unittest.main()
