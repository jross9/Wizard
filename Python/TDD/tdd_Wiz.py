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
		self.assertEqual(folder.Folder, folder.Sln); 
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

	def test_XML_Read_File_Node(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		# -----------------------------------------
		self.assertEqual(len(folder.Files), 0)
		# -----------------------------------------
		node = Et.fromstring('''
			<Folder>
				<File ID="File.txt" />
			</Folder>
		''')
		folder.ReadXML(node)
		# -----------------------------------------
		self.assertEqual(len(folder.Files), 1)
		self.assertEqual(folder.Files[0].ID, 'File.txt')
		self.assertIsInstance(folder.Files[0], Wiz.File)

	def test_XML_Read_Folder_Node(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		# -----------------------------------------
		self.assertEqual(len(folder.Folders), 0)
		# -----------------------------------------
		node = Et.fromstring('''
			<Folder>
				<Folder ID="SubFolder" />
			</Folder>
		''')
		folder.ReadXML(node)
		# -----------------------------------------
		self.assertEqual(len(folder.Folders), 1)
		self.assertEqual(folder.Folders[0].ID, 'SubFolder')

	def test_XML_Read_SubFolder_And_File_Node(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		# -----------------------------------------
		self.assertEqual(len(folder.Files), 0)
		self.assertEqual(len(folder.Folders), 0)
		# -----------------------------------------
		node = Et.fromstring('''
			<Folder>
				<Folder ID="SubFolder">
					<Folder ID="SubFolder2">
						<File ID="File.txt" />
					</Folder>
					<File ID="File2.txt" />
				</Folder>
			</Folder>
		''')
		folder.ReadXML(node)
		# -----------------------------------------
		self.assertEqual(len(folder.Folders), 1)
		self.assertEqual(folder.Folders[0].ID, 'SubFolder')
		# -----------------------------------------
		self.assertEqual(len(folder.Folders[0].Folders), 1)
		fldr = folder.Folders[0].Folders[0]
		self.assertEqual(fldr.ID, 'SubFolder2')
		self.assertEqual(fldr.FolderPath, folder.Sln.FolderPath + '/Folder/SubFolder/SubFolder2')
		# -----------------------------------------
		self.assertEqual(len(folder.Folders[0].Folders[0].Files), 1)
		file = folder.Folders[0].Folders[0].Files[0]
		self.assertEqual(file.ID, 'File.txt')
		self.assertEqual(file.FilePath, folder.Sln.FolderPath + '/Folder/SubFolder/SubFolder2/File.txt')
		# -----------------------------------------
		self.assertEqual(len(folder.Folders[0].Files), 1)
		file = folder.Folders[0].Files[0]
		self.assertEqual(file.ID, 'File2.txt')
		self.assertEqual(file.FilePath, folder.Sln.FolderPath + '/Folder/SubFolder/File2.txt')

	def test_XML_Write_Nodes(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		Wiz.File.MAKE('File.txt', folder)
		Wiz.Folder.MAKE('Folder', folder)
		# -----------------------------------------
		stream = io.StringIO()
		writer = Xml.TextWriter(stream)
		folder.WriteXML(writer)
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Folder ID="Folder">', 
			'\t<Folder ID="Folder" />',
			'\t<File ID="File.txt" />',
			'</Folder>']))

# ---------------------------------------------------------------------
# File
# ---------------------------------------------------------------------
class File_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		file = Wiz.File.MAKE('File.txt', sln)
		# -----------------------------------------
		self.assertEqual(file.IsFolder, False)
		# -----------------------------------------
		self.assertEqual(file.ID, 'File.txt')
		self.assertEqual(file.FileName, 'File')
		self.assertEqual(file.FileExt, '.txt')
		self.assertEqual(file.FilePath, file.Sln.FolderPath + '/' + file.ID)
		self.assertEqual(file.XmlName, 'File')
		# -----------------------------------------
		self.assertEqual(file.FolderPath, file.Sln.FolderPath)
		# -----------------------------------------
		self.assertEqual(file.Folder, file.Sln) # NULL because we don't know what we are yet ...
		self.assertEqual(file.DefNamespace, 'Solution')

	def test_File_In_Folder(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder.MAKE('Folder', sln)
		file = Wiz.File.MAKE('File.txt', folder)
		# -----------------------------------------
		self.assertEqual(file.FolderPath, file.Sln.FolderPath + '/Folder')
		# -----------------------------------------
		self.assertEqual(file.Folder, folder)
		self.assertEqual(file.DefNamespace, 'Solution.Folder')

	def test_File_No_Extension(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		file = Wiz.File.MAKE('FileNoExt', sln)
		# -----------------------------------------
		self.assertEqual(file.ID, 'FileNoExt')
		self.assertEqual(file.FileName, 'FileNoExt')
		self.assertEqual(file.FileExt, '')

	def test_XML_Read_Attributes(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		file = Wiz.File.MAKE('File.txt', sln)
		# -----------------------------------------
		node = Et.fromstring('<File Mko="Test/Test.txt" CopySource="Y" />')
		file.ReadXML(node)

	def test_XML_Write_Attributes(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		file = Wiz.File.MAKE('File.txt', sln)
		# -----------------------------------------
		file.MkoFilePath = 'Test/Test.txt'
		file.CopySource = True
		# -----------------------------------------
		stream = io.StringIO()
		writer = Xml.TextWriter(stream)
		# -----------------------------------------
		file.WriteXML(writer)
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), '<File ID="File.txt" Mko="Test/Test.txt" />\n')

# ---------------------------------------------------------------------
# Module
# ---------------------------------------------------------------------
class Module_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		mod = Wiz.Module.MAKE('Module.xyz', sln)
		# -----------------------------------------
		# self.assertEqual(mod.ID, 'Module.txt')
		# self.assertEqual(mod.XmlName, 'Module')
		# self.assertEqual(mod.DstXmlPath, G.WizPrjDir + '/' + mod.Sln.ID + '/__wiz__/' + mod.ID + '.xml')
		# self.assertEqual(mod.SrcXmlPath, G.WizPrjDir + '/' + mod.Sln.ID + '2/__wiz__/' + mod.ID + '.xml')
		# -----------------------------------------
		# mod = Wiz.Module.Create('ModNoExt', mod.Sln)
		# self.assertEqual(mod.DstXmlPath, G.WizPrjDir + '/' + mod.Sln.ID + '/__wiz__/ModNoExt.xml')
		# self.assertEqual(mod.SrcXmlPath, G.WizPrjDir + '/' + mod.Sln.ID + '2/__wiz__/' + mod.ID + '.xml')
		# -----------------------------------------
		tgt = Wiz.Target.MAKE('Target', mod.Sln)
		mod = Wiz.Module.MAKE('Module.xyz', tgt)
		# -----------------------------------------
		self.assertEqual(mod.DstXmlPath, G.WizPrjDir + '/' + mod.Sln.ID + '/__wiz__/' + mod.Tgt.ID + '/' + mod.ID + '.xml')
		self.assertEqual(mod.SrcXmlPath, G.WizPrjDir + '/' + mod.Sln.ID + '2/__wiz__/' + mod.Tgt.ID + '/' + mod.ID + '.xml')

	def test_Mako_Template(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		mod = Wiz.Module.MAKE('Module.txt', sln)
		# -----------------------------------------
		self.assertIsNone(mod.MkoFilePath)
		self.assertIsNone(mod.S)
		# -----------------------------------------
		mod.MkoFilePath = 'Test/Test.txt.mako'
		# -----------------------------------------
		mod.CreateIt()
		# -----------------------------------------
		self.assertIsNotNone(mod.S.MkoTemplate)
		# -----------------------------------------
		sb = []
		sb.append('Test Mako Template')
		sb.append('Solution=Solution')
		sb.append('ID=Module.txt!!')
		# -----------------------------------------
		self.assertEqual(mod.S.ToStr(), UT.List2StrSrc(mod.S, sb))

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
