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
		self.assertEqual(mod.ID, 'Module.xyz')
		self.assertEqual(mod.XmlName, 'Module')
		self.assertEqual(mod.XmlPath, G.Temp + '/' + mod.Sln.ID + '/__wiz__/' + mod.ID + '.xml')
		# -----------------------------------------
		mod = Wiz.Module.MAKE('ModNoExt', mod.Sln)
		self.assertEqual(mod.XmlPath, G.Temp + '/' + mod.Sln.ID + '/__wiz__/ModNoExt.xml')
		# -----------------------------------------
		tgt = Wiz.Target.MAKE('Target', mod.Sln)
		mod = Wiz.Module.MAKE('Module.xyz', tgt)
		# -----------------------------------------
		self.assertEqual(mod.XmlPath, G.Temp + '/' + mod.Sln.ID + '/__wiz__/' + mod.Tgt.ID + '/' + mod.ID + '.xml')

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

# ---------------------------------------------------------------------
# Target 
# ---------------------------------------------------------------------
class Target_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		# -----------------------------------------
		self.assertEqual(tgt.ID, 'Target')
		self.assertEqual(tgt.Tgt, tgt)

	def test_Namespaces(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		# -----------------------------------------
		self.assertEqual(tgt.Namespace, 'Target')

	def test_Namespaces2(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		tgt._namespace = 'AltNS'
		# -----------------------------------------
		self.assertEqual(tgt.Namespace, 'AltNS')

	def test_Namespaces3(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		tgt._namespace = 'AltNS'
		# -----------------------------------------
		mod = Wiz.Module.MAKE('Module.txt', tgt)
		self.assertEqual(mod.Namespace, 'AltNS')
		# -----------------------------------------
		sub_folder = Wiz.Folder.MAKE('Folder', tgt)
		self.assertEqual(sub_folder.Namespace, 'AltNS.Folder')
		# -----------------------------------------
		mod2 = Wiz.Module.MAKE('Module.txt', sub_folder)
		self.assertEqual(mod2.Namespace, 'AltNS.Folder')

	def test_Namespaces4(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		# -----------------------------------------
		mod = Wiz.Module.MAKE('Module.txt', tgt)
		mod._namespace = 'OtherNS'
		# -----------------------------------------
		self.assertEqual(mod.Namespace, 'OtherNS')

	def test_Xml_Write_Solution_Attributes(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		tgt = Wiz.Target.MAKE('Target', sln)
		# -----------------------------------------
		stream = io.StringIO()
		writer = Xml.TextWriter(stream)
		tgt.WriteXML(writer)
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), '<Target ID="Target" />\n')
		# -----------------------------------------
		tgt.Guid = uuid.UUID('{9159B9D4-1E42-41DF-8E27-46B8D9F0ED73}')
		tgt.PrivPrefix = 'p_'
		tgt.CtrlPrefix = 'Widget'
		tgt.ViewPrefix = 'Form'
		# -----------------------------------------
		stream = io.StringIO()
		writer = Xml.TextWriter(stream)
		tgt.WriteXML(writer)
		# -----------------------------------------
		# self.assertEqual(stream.getvalue(), '<Target ID="Target" Guid="9159B9D4-1E42-41DF-8E27-46B8D9F0ED73" PrivPrefix="p_" CtrlPrefix="Widget" ViewPrefix="Form" />\n')
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Target ID="Target"', 
			'\tGuid="9159B9D4-1E42-41DF-8E27-46B8D9F0ED73"',
			'\tPrivPrefix="p_" CtrlPrefix="Widget" ViewPrefix="Form" />']))

# ---------------------------------------------------------------------
# Solution 
# ---------------------------------------------------------------------
class Solution_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		# -----------------------------------------
		self.assertEqual(sln.ID, 'Solution')
		self.assertEqual(sln.XmlName, 'Solution')
		self.assertEqual(sln.DefNamespace, 'Solution')
		# -----------------------------------------
		self.assertEqual(sln.VSDefVer, G.VSVers.VS2008)
		self.assertEqual(sln.FWDefVer, G.FWVers.Net35)
		# -----------------------------------------
		self.assertEqual(sln.DefRootPath, G.Temp + '/Solution')
		self.assertEqual(sln.RootPath, G.Temp + '/Solution')
		# -----------------------------------------
		self.assertEqual(sln.FolderPath, G.Temp + '/Solution')
		# -----------------------------------------
		self.assertEqual(sln.XmlPath, sln.FolderPath + '/' + sln.ID + '.xml')
		# -----------------------------------------
		self.assertEqual(sln.XmlPath, G.Temp + '/Solution/Solution.xml')
		# -----------------------------------------
		self.assertEqual(sln.XmlFolderPath, G.Temp + '/' + sln.ID + '/__wiz__')
		# -----------------------------------------
		self.assertEqual(sln.Sln, sln)

	def test_SubSolution(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		sub_sln = Wiz.Solution('SubSolution', parent=sln)
		# -----------------------------------------
		self.assertEqual(sub_sln.DefNamespace, 'Solution.SubSolution')
		# -----------------------------------------
		self.assertEqual(sub_sln.FolderPath, sln.FolderPath + '/SubSolution')
		self.assertEqual(sub_sln.RootPath, G.Temp + '/Solution/SubSolution')

	def test_SubFolderSubSolution(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		folder = Wiz.Folder(sln)
		folder.SetID('Folder')
		sub_sln = Wiz.Solution('SubSolution', parent=folder)
		# -----------------------------------------
		self.assertEqual(sub_sln.DefNamespace, 'Solution.Folder.SubSolution')
		# -----------------------------------------
		self.assertEqual(sub_sln.FolderPath, folder.FolderPath + '/SubSolution')
		self.assertEqual(sub_sln.RootPath, G.Temp + '/Solution/Folder/SubSolution')

	def test_Add_Target(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		# -----------------------------------------
		tgt = Wiz.Target(sln)
		tgt.SetID('Target')
		tgt2 = Wiz.Target(sln)
		tgt2.SetID('Target2')
		# -----------------------------------------
		self.assertEqual(len(sln.Targets), 0)
		# -----------------------------------------
		sln.AddTarget(tgt)
		self.assertEqual(len(sln.Targets), 1)
		sln.AddTarget(tgt2)
		self.assertEqual(len(sln.Targets), 2)
		# -----------------------------------------
		self.assertEqual(sln.Targets[0], tgt)
		self.assertEqual(sln.Targets[1], tgt2)

	def test_XML_Read_Attributes(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		# -----------------------------------------
		node = Et.fromstring('<Solution VS="VS2005" FW="Net20" />')
		sln.ReadXML(node)
		self.assertEqual(sln.VSDefVer, G.VSVers.VS2005)
		self.assertEqual(sln.FWDefVer, G.FWVers.Net20)
		# -----------------------------------------
		node = Et.fromstring('<Solution VS="VS2008" FW="Net35" />')
		sln.ReadXML(node)
		self.assertEqual(sln.VSDefVer, G.VSVers.VS2008)
		self.assertEqual(sln.FWDefVer, G.FWVers.Net35)
		# -----------------------------------------
		node = Et.fromstring('<Solution VS="VS2010" FW="Net40" />')
		sln.ReadXML(node)
		self.assertEqual(sln.VSDefVer, G.VSVers.VS2010)
		self.assertEqual(sln.FWDefVer, G.FWVers.Net40)
		# -----------------------------------------
		node = Et.fromstring('<Solution VS="VS2012" FW="Net45" />')
		sln.ReadXML(node)
		self.assertEqual(sln.VSDefVer, G.VSVers.VS2012)
		self.assertEqual(sln.FWDefVer, G.FWVers.Net45)

	def test_XML_Read_File_Node(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		# -----------------------------------------
		self.assertEqual(len(sln.Files), 0)
		# -----------------------------------------
		node = Et.fromstring('''
			<Solution>
				<File ID="Test.txt" />
			</Solution>
		''')
		sln.ReadXML(node)
		# -----------------------------------------
		self.assertEqual(len(sln.Files), 1)

	def test_XML_Read_Folder_Node(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		# -----------------------------------------
		self.assertEqual(len(sln.Folders), 0)
		# -----------------------------------------
		node = Et.fromstring('''
			<Solution>
				<Folder ID="Folder">
					<File ID="Test.txt" />
				</Folder>
			</Solution>
		''')
		sln.ReadXML(node)
		# -----------------------------------------
		self.assertEqual(len(sln.Folders), 1)
		self.assertEqual(len(sln.Folders[0].Files), 1)

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
