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
import CS.Lib

# ---------------------------------------------------------------------
# Folder
# ---------------------------------------------------------------------
class Target_Tests(unittest.TestCase):

	def test_Xml_Read_Target(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		# -----------------------------------------
		self.assertEqual(len(sln.Targets), 0)
		self.assertEqual(len(sln.TargetDict), 0)
		# -----------------------------------------
		node = Et.fromstring('''
			<Solution>
				<CSharp.Lib ID="CSLib" />
			</Solution>
		''')
		sln.ReadXML(node)
		# -----------------------------------------
		self.assertEqual(len(sln.Targets), 1)
		self.assertEqual(len(sln.TargetDict), 1)
		# -----------------------------------------
		self.assertEqual(sln.Targets[0].ID, 'CSLib')
		self.assertIsInstance(sln.Targets[0], CS.Lib.Target)


# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	G.LogCount('tdd_CS', 'Unit (Python)')
	# -----------------------------------------------------------------
	Dbg.LogOff = True
	# -----------------------------------------------------------------
	unittest.main()
