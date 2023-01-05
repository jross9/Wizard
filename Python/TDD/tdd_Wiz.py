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

# ---------------------------------------------------------------------
# Folder
# ---------------------------------------------------------------------
class Folder_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		# -----------------------------------------
		self.assertEqual(folder.ID, 'Folder')
		self.assertEqual(folder.XmlName, 'Folder')
		# -----------------------------------------
		self.assertEqual(folder.IsFolder, True)
		# -----------------------------------------
		self.assertEqual(len(folder.Sln.FSNodes), 1)
		self.assertEqual(folder.Sln.FSNodes[0], folder)
		self.assertEqual(len(folder.Sln.Folders), 1)
		# -----------------------------------------
		self.assertEqual(len(folder.FSNodes), 0)
		self.assertEqual(len(folder.Folders), 0)
		self.assertEqual(len(folder.Files), 0)
		# -----------------------------------------
		self.assertEqual(folder.FolderPath, folder.Sln.FolderPath + '/Folder')
		# -----------------------------------------
		self.assertEqual(folder.Folder, folder.Sln); # IFolder -- NULL because we don't know what we are yet ...
		self.assertEqual(folder.DefNamespace, 'Solution.Folder')

	def test_Folder_In_Folder(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		sub_folder = Wiz.Folder.MAKE('SubFolder', folder)
		# -----------------------------------------
		self.assertEqual(len(folder.FSNodes), 1)
		self.assertEqual(folder.FSNodes[0], sub_folder)
		# -----------------------------------------
		self.assertEqual(sub_folder.ID, 'SubFolder')
		# -----------------------------------------
		self.assertEqual(sub_folder.FolderPath, sln.FolderPath + '/Folder/SubFolder')
		# -----------------------------------------
		self.assertEqual(sub_folder.DefNamespace, 'Solution.Folder.SubFolder')

	def test_Folder_In_Target(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		folder = Wiz.Folder.MAKE('Folder', tgt)
		# -----------------------------------------
		self.assertEqual(folder.FolderPath, folder.Sln.FolderPath + '/Target/Folder')
		# -----------------------------------------
		self.assertEqual(folder.DefNamespace, 'Target.Folder')

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
