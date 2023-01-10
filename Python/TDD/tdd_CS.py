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
# 
# ---------------------------------------------------------------------
class Module_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		mod = CS.Module.MAKE('Module.cs', sln)
		# -----------------------------------------
		self.assertEqual(mod.ID, 'Module.cs')

	def test_Default_Mako_Template(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		mod = CS.Module.MAKE('Module.cs', tgt)
		# -----------------------------------------
		mod.MkoFilePath = 'CS/Module.cs.mako'
		# -----------------------------------------
		mod.CreateIt()
		# -----------------------------------------
		sb = []
		sb.append('using System;')
		sb.append('using System.Collections.Generic;')
		sb.append('using System.Text;')
		sb.append('')
		sb.append('namespace Target')
		sb.append('{')
		sb.append('\t// Solution -> Solution')
		sb.append('\t// Module -> ' + G.Temp + '/Solution/Target/Module.cs')
		sb.append('\t// Target -> Target')
		sb.append('}')
		# -----------------------------------------
		self.assertEqual(mod.S.ToStr(), UT.List2StrSrc(mod.S, sb))

# ---------------------------------------------------------------------
class AssemblyInfo_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		mod = CS.AssemblyInfoModule.MAKE('AssemblyInfo.cs', sln)
		# -----------------------------------------
		self.assertEqual(mod.ID, 'AssemblyInfo.cs')

# ---------------------------------------------------------------------
# Folder
# ---------------------------------------------------------------------
class Folder_Tests(unittest.TestCase):

	def test_XML_Read_Module_Node(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		# -----------------------------------------
		self.assertEqual(len(folder.Files), 0)
		self.assertEqual(len(folder.Sln.Modules), 0)
		# -----------------------------------------
		node = Et.fromstring('''
			<Folder>
				<CSharp.Module ID="Test.cs" />
			</Folder>
		''')
		folder.ReadXML(node)
		# -----------------------------------------
		self.assertEqual(len(folder.Files), 1)
		self.assertEqual(len(folder.Sln.Modules), 1)
		# -----------------------------------------
		self.assertEqual(folder.Files[0].ID, 'Test.cs')
		self.assertIsInstance(folder.Files[0], CS.Module)

# ---------------------------------------------------------------------
# Target
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
