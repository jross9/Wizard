#
# Copyright James Ross (C) 2023
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
from __future__ import annotations
from typing import List, Dict


import os
# import shutil
import xml.etree.ElementTree as Et
from llist import dllist, dllistnode
import mako.template as Mko


# =====================================================================
# Lang -> Wiz.py
# =====================================================================
import Glb as G
import Base
import Dbg
import Xml

# =====================================================================
# WizObj
# =====================================================================
class WizObj(Base.BaseObj):

	def __init__(self, parent):
		# -----------------------------------------
		self._tgt = None 
		# -----------------------------------------
		super().__init__(parent)
		# -----------------------------------------
		self.BuildFlg = False
		# -----------------------------------------
		if isinstance(parent, Target):
			self._tgt = parent
		elif isinstance(parent, WizObj):
			self._tgt = parent.Tgt

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def Tgt(self): 
		return self._tgt

	# ---------------------------------------------
	# BUILD
	# ---------------------------------------------
	def BuildTarget(self, xObj:WizObj=None):
		# -----------------------------------------
		if self.BuildFlg:
			raise Exception('BUILD ALREADY CALLED!! ' + str(self))
		# -----------------------------------------
		self.BuildFlg = True

# =====================================================================
# AstNode
# =====================================================================
class AstNode(WizObj):

	NodeCount = 0

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		AstNode.NodeCount += 1
		# -----------------------------------------
		self.Node:dllistnode = None
		# -----------------------------------------
		self.EmptyLine = False
		# -----------------------------------------
		self.EolCommment:str = None # string
		self.EolCommentIdx = 0  # int 

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): 
		return 'Node'

	@property
	def ParentBlock(self):
		# -----------------------------------------
		if (isinstance(self.Parent, AstBlock)):
			return self.Parent
		else:
			return self.Parent.ParentBlock

	@property
	def ParentModule(self):
		# -----------------------------------------
		if (isinstance(self.Parent, Module)):
			return self.Parent
		else:
			return self.Parent.ParentModule
	
	# ---------------------------------------------
	# XML
	# ---------------------------------------------
	def WriteXML(self, writer):
		# -----------------------------------------
		writer.WriteStartElement(self.XmlName)
		self.XmlWriteAttributes(writer)
		if (self.EmptyLine):
			writer.WriteAttributeString('EL', 'Y')
		self.XmlWriteNodes(writer)
		writer.WriteEndElement()

	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('EL' in node.attrib):
			self.EmptyLine = True

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)

	# ---------------------------------------------
	# CREATE
	# ---------------------------------------------
	def Source_Code(self, S):
		# -----------------------------------------
		S.Code(';; Z.AstNode::Source_Code: ' + str(self))
		# -----------------------------------------
		for node in self.NodeList:
			node.Source_Code(S)

# ---------------------------------------------------------------------
class AstBlock(AstNode):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.NodeList = dllist() # LinkedList<AstNode>
		# -----------------------------------------
		self.EnumTypeDict = {}
		# -----------------------------------------
		self.Data = []
		self.DataDict = {}
		# -----------------------------------------
		self.Methods = []
		self.MethodDict = {}
		# -----------------------------------------
		self.Classes = []
		self.ClassDict = {}

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): 
		return 'Block'

	# ---------------------------------------------
	# NEW
	# ---------------------------------------------
	def New_LineComment(self):
		# -----------------------------------------
		raise Exception('Must override New_LineComment')

	# ---------------------------------------------
	# METHODS
	# ---------------------------------------------
	def AddNode(self, node):
		# -----------------------------------------
		node.Node = self.NodeList.append(node)

	def AddToContext(self, node):
		# -----------------------------------------
		self.AddNode(node)

	def AddData(self, data):
		# -----------------------------------------
		self.Data.append(data)
		G.SetKey(data.ID, data, self.DataDict)

	def AddMethod(self, meth):
		# -----------------------------------------
		self.Methods.append(meth)
		G.SetKey(meth.ID, meth, self.MethodDict)

	def AddClass(self, cls):
		# -----------------------------------------
		self.Classes.append(cls)
		G.SetKey(cls.ID, cls, self.ClassDict)

	# ---------------------------------------------
	# XML
	# ---------------------------------------------
	def XmlReadNode(self, node):
		# -----------------------------------------
		if (node.tag == 'LineComment'):
			# -------------------------------------
			ast = self.New_LineComment()
			ast.ReadXML(node)
			self.AddToContext(ast)
		# -----------------------------------------
		else:
			super().XmlReadNode(node)

	def XmlWriteNodes(self, writer):
		super().XmlWriteNodes(writer)
		# -----------------------------------------
		for node in self.NodeList:
			node.WriteXML(writer)

# =====================================================================
# Comments
# =====================================================================
# =====================================================================
# Comments
# =====================================================================
class Comment(AstNode):

	def __init__(self, parent):
		super().__init__(parent)

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): 
		return 'Comment'

# ---------------------------------------------------------------------
class LineComment(Comment):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.Comment:str = None

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): 
		return 'LineComment'

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('Comment' in node.attrib):
			self.Comment = node.attrib['Comment'] 

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		if (self.Comment != None):
			writer.WriteAttributeString('Comment', self.Comment)

	# ---------------------------------------------
	# CREATE
	# ---------------------------------------------
	def Source_Code(self, S):
		# -----------------------------------------
		S.Code(';; ' + str(self.Comment))
		# -----------------------------------------
		if (self.EmptyLine):
			S.Blank()

# ---------------------------------------------------------------------
class BlockComment(Comment):

	def __init__(self, parent):
		super().__init__(parent)

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): 
		return 'BlockComment'

# =====================================================================
# FSNode / File / Folder
# =====================================================================
class FSNode(Base.IDObj, WizObj):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.Folder = self.Parent
		# -----------------------------------------
		self.CreateFlg = False
		self.SaveFlg = False
		# -----------------------------------------
		self._namespace = None

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def IsFolder(self): 
		return False

	# ---------------------------------------------
	@property
	def FolderPath(self): 
		# -----------------------------------------
		return self.Folder.FolderPath

	@property
	def DefNamespace(self): 
		# -----------------------------------------
		return self.Folder.DefNamespace

	@property
	def DottedPath(self): 
		# -----------------------------------------
		return self.Folder.DottedPath + '.' + self.ID

	@property
	def Namespace(self): 
		# -----------------------------------------
		if (self._namespace != None):
			return self._namespace
		else:
			return self.Folder.Namespace

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('Namespace' in node.attrib):
			self._namespace = node.attrib['Namespace']

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		if (self._namespace != None):
			writer.WriteAttributeString('Namespace', self._namespace)
	
	# ---------------------------------------------
	# CREATE
	# ---------------------------------------------
	def CreateIt(self):
		# -----------------------------------------
		if (self.CreateFlg):
			raise Exception('Node already Created! ' + self.ID)
		# -----------------------------------------
		self.CreateFlg = True

	def SaveIt(self):
		# -----------------------------------------
		if (self.SaveFlg):
			raise Exception('Node already Saved! ' + self.ID)
		# -----------------------------------------
		self.SaveFlg = True

# ---------------------------------------------------------------------
class File(FSNode):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.Name = None
		# -----------------------------------------
		self.FileName = None
		self.FileExt = None
		# -----------------------------------------
		self.S = None # Source
		self.IsEmbeddedCode = False
		self.MkoFilePath = None

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, parent:Folder, mko:str=None) -> File:
		# -----------------------------------------
		file = File(parent)
		file.SetID(iD)
		parent.AddFile(file)
		file.MkoFilePath = mko or file.MkoFilePath
		# -----------------------------------------
		return file

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): 
		return 'File'

	# ---------------------------------------------
	@property
	def FilePath(self):
		# -----------------------------------------
		return self.Folder.FolderPath + '/' + self.ID

	# ---------------------------------------------
	def SetID(self, iD):
		super().SetID(iD)
		# -----------------------------------------
		self.Name = self.ID.split('.')[0]
		# -----------------------------------------
		file_name, file_extension = os.path.splitext(iD)
		self.FileName = file_name
		self.FileExt = file_extension

	# ---------------------------------------------
	# METHODS
	# ---------------------------------------------
	def NewSource(self):
		# -----------------------------------------
		return Base.Source()  # return this lang XX.Src

	def NewSrcT(self, S):
		# -----------------------------------------
		T = self.NewSource() # should get overriden
		T.TabLevel = S.TabLevel
		# -----------------------------------------
		return T

	def NewSrcT1(self, S):
		# -----------------------------------------
		T = self.NewSource() # should get overriden
		T.TabLevel = S.TabLevel + 1
		# -----------------------------------------
		return T

	def InitSource(self):
		# -------------------------------------
		self.S = self.NewSource()
		self.S.FilePath = self.FilePath

	def MakoSource(self, ctx) -> Base.MakoSource:
		# -------------------------------------
		S = Base.MakoSource(ctx)
		return S

	def Source_Code(self, S):
		# -----------------------------------------
		pass

	def TestContext(self, ctx):
		return 'How it\'s done! --> ' + str(ctx)

	def TestContext2(self, ctx):
		ctx.write('Line 1\r\n')
		ctx.write('Line 2\r\n')
		ctx.write('Line 3\r\n')

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('ECT' in node.attrib):
			self.IsEmbeddedCode = True
		# -----------------------------------------
		if ('Mko' in node.attrib):
			self.MkoFilePath = node.attrib['Mko'] 

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		if (self.MkoFilePath != None):
			writer.WriteAttributeString('Mko', self.MkoFilePath)
		# -----------------------------------------
		elif (self.IsEmbeddedCode):
			writer.WriteAttributeString('ECT', 'Y')

	# ---------------------------------------------
	# CREATE
	# ---------------------------------------------
	def CreateIt(self):
		super().CreateIt()
		# -----------------------------------------
		self.InitSource()
		# -----------------------------------------
		if (self.MkoFilePath != None):
			# -------------------------------------
			mko_file = G.MkoDefRoot + '/' + self.MkoFilePath
			# -------------------------------------
			if (os.path.isfile(mko_file)):
				# -------------------------------------
				self.S.MkoTemplate = Mko.Template(filename = mko_file, module_directory = G.MkoTmpFolder)
				# -------------------------------------
				self.SetMkoAttribs()
			else:
				# -------------------------------------
				raise Exception('Mako Template does not exist: [' + mko_file + ']')
		# -----------------------------------------
		elif (self.IsEmbeddedCode): 
			self.Header(self.S)
			self.BodyBegin(self.S)
			self.Body(self.S)
			self.BodyEnd(self.S)
		# -----------------------------------------
		else:
			self.CreateSource()

	def SetMkoAttribs(self):
		# -----------------------------------------
		self.S.MkoAttribs['sln'] = self.Sln
		# -------------------------------------
		if (self.Tgt != None):
			self.S.MkoAttribs['tgt'] = self.Tgt
		# -------------------------------------
		self.S.MkoAttribs['file'] = self

	def Header(self, S):
		# -----------------------------------------
		pass

	def BodyBegin(self, S):
		# -----------------------------------------
		pass

	def Body(self, S):
		# -----------------------------------------
		pass

	def BodyEnd(self, S):
		# -----------------------------------------
		pass

	def CreateSource(self):
		# -----------------------------------------
		self.Source_Code(self.S)

	def SaveIt(self):
		super().SaveIt()
		# -----------------------------------------
		self.S.Save(self.DstFilePath)

# ---------------------------------------------------------------------
class Folder(FSNode):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.IsVirtual = False
		self.UseParentNS = False
		# -----------------------------------------
		self.FSNodes = []
		# -----------------------------------------
		self.Folders = []
		self.FolderDict = {}
		# -----------------------------------------
		self.Files = []
		self.FileDict = {}

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, parent:Folder) -> Folder:
		# -----------------------------------------
		folder = Folder(parent)
		folder.SetID(iD)
		parent.AddFolder(folder)
		# -----------------------------------------
		return folder

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): 
		return 'Folder'

	@property
	def IsFolder(self): 
		return True

	@property
	def FolderPath(self): 
		# -----------------------------------------
		if (self.IsVirtual):
			return self.Folder.FolderPath
		else:
			return self.Folder.FolderPath + '/' + self.ID

	# ---------------------------------------------
	@property
	def XmlFolderPath(self): 
		# -----------------------------------------
		if (self.IsVirtual):
			return self.Folder.XmlFolderPath
		else:
			return self.Folder.XmlFolderPath + '/' + self.ID

	@property
	def DefNamespace(self): 
		# -----------------------------------------
		if (self.UseParentNS):
			return self.Parent.DefNamespace
		else:  
			return self.Folder.DefNamespace + '.' + self.ID

	@property
	def Namespace(self): 
		# -----------------------------------------
		if (self._namespace != None):
			return self._namespace
		else:
			if (self.UseParentNS):
				return self.Parent.Namespace
			else:
				return self.Folder.Namespace + '.' + self.ID

	# ---------------------------------------------
	# METHODS
	# ---------------------------------------------
	def AddFile(self, file:File):
		# -----------------------------------------
		if (file.Parent != self):
			raise Exception('BAD Container Parent')
		# -----------------------------------------
		self.FSNodes.append(file)  # JAR_NOTE: Revisit (C#X I was not doing this)
		# -----------------------------------------
		self.Files.append(file)
		G.SetKey(file.ID, file, self.FileDict)
		# -----------------------------------------
		# JAR_NOTE: add Solution AllFilesDict
		# this.Sln.AllFilesDict.Add(file.DottedPath, file);
		# -----------------------------------------
		pass
	
	def AddFolder(self, folder:Folder):
		# -----------------------------------------
		if (folder.Parent != self):
			raise Exception('BAD Container Parent: ' + str(folder.Parent))
		# -----------------------------------------
		self.FSNodes.append(folder) # JAR_NOTE: Revisit (C#X I was not doing this)
		# -----------------------------------------
		self.Folders.append(folder)
		G.SetKey(folder.ID, folder, self.FolderDict)

	def AddModule(self, mod:Module):
		# -----------------------------------------
		self.AddFile(mod)
		# -----------------------------------------
		if (isinstance(self, Target) or 
		    isinstance(self, Solution)):
			fldr = self
		elif (self.Tgt != None):
			fldr = self.Tgt
		else:
			fldr = self.Sln
		# -----------------------------------------
		fldr.Modules.append(mod)
		G.SetKey(mod.FilePath, mod, fldr.ModuleDict)

	def AddTarget(self, tgt:Target):
		# -----------------------------------------
		# JAR_NOTE: this check will happen in AddFolder I can safely remove it
		if (tgt.Parent != self):
			raise Exception('BAD Container Parent: ' + str(tgt.Parent))
		# -----------------------------------------
		self.AddFolder(tgt)
		# -----------------------------------------
		# JAR_NOTE: Change below
		# tgt.Sln.Targets.Add(tgt);
		# tgt.Sln.TargetDict.Add(tgt.DottedPath, tgt);
		# -----------------------------------------
		sln = tgt.Sln
		if isinstance(self, Solution):
			sln = self
		sln.Targets.append(tgt)
		G.SetKey(tgt.DottedPath, tgt, sln.TargetDict)

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('UseParentNS' in node.attrib):
			self.UseParentNS = True

	def XmlReadNode(self, node):
		# =========================================
		#
		# =========================================
		if (node.tag == 'File'):
			# -------------------------------------
			file = File.MAKE(node.attrib['ID'], self)
			file.ReadXML(node)
		# -----------------------------------------
		elif (node.tag == 'Folder'):
			# -------------------------------------
			folder = Folder.MAKE(node.attrib['ID'], self)
			folder.ReadXML(node)
		# =========================================
		#
		# =========================================
		#elif (node.tag.startswith('Cpp.')):
		#	# -------------------------------------
		#	import C.Cpp
		#	C.Cpp.Target.XmlReadNodes(node, self) 
		# -----------------------------------------
		elif (node.tag.startswith('CSharp.')):
			# -------------------------------------
			import CS
			CS.Target.XmlReadNodes(node, self) 
		# -----------------------------------------
		#elif (node.tag.startswith('PyAST.')):
		#	# -------------------------------------
		#	import PyAST
		#	PyAST.Target.XmlReadNodes(node, self) 
		# -----------------------------------------
		#elif (node.tag.startswith('VS.')):
		#	# -------------------------------------
		#	import VS
		#	VS.XmlReadNodes(node, self) 
		# -----------------------------------------
		else:
			raise Base.UnknowNodeException('Bad NODE Tag [' + node.tag + ']')

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		if (self.UseParentNS):
			writer.WriteAttributeString('UseParentNS', 'Y')

	def XmlWriteNodes(self, writer):
		super().XmlWriteNodes(writer)
		# -----------------------------------------
		for nodes in self.Folders:
			nodes.WriteXML(writer)
		for nodes in self.Files:
			nodes.WriteXML(writer)

# =====================================================================
# Module
# =====================================================================
class Module(File, AstBlock):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.SeparateXmlFile = False 
		# -----------------------------------------
		# self.HaxeModule = None

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def Lang(self): 
		return G.Lang.NA

	@property
	def XmlName(self): 
		return 'Module'

	@property
	def XmlPath(self):
		# -----------------------------------------
		return self.Folder.XmlFolderPath + '/' + self.ID + '.xml'

	# ---------------------------------------------
	# XML 
	# ---------------------------------------------
	def ReadXML(self, node):
		# -----------------------------------------
		self.XmlReadAttributes(node)
		self.ReadXmlFile()

	def WriteXML(self, writer):
		# -----------------------------------------
		writer.WriteStartElement(self.XmlName)
		self.XmlWriteAttributes(writer)
		self.WriteXmlFile()
		writer.WriteEndElement()

	# ---------------------------------------------
	# XML Doc
	# ---------------------------------------------
	def ReadXmlFile(self):
		# -----------------------------------------
		if (not os.path.exists(self.SrcXmlPath)):
			Dbg.Warn('Project XML File Not Found: ' + self.SrcXmlPath)
			return
		# -----------------------------------------
		tree = Et.ElementTree()
		tree.parse(self.SrcXmlPath)
		root = tree.getroot()
		# -----------------------------------------
		for subnode in root:
			self.XmlReadNode(subnode);

	def WriteXmlFile(self):
		# -----------------------------------------
		if (not os.path.exists(self.Folder.XmlFolderPath)):
			os.makedirs(self.Folder.XmlFolderPath)
		# -----------------------------------------
		stream = open(self.DstXmlPath, 'wt')
		writer = Xml.TextWriter(stream)
		writer.WriteStartElement(self.XmlName)
		writer.WriteAttributeString('ID', self.ID)
		self.XmlWriteNodes(writer)
		writer.WriteEndElement()
		stream.close()

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		#if ('XPrj' in node.attrib):
		#	xPrjStr = node.attrib['XPrj']
		#	self.XPrj = self.Sln.ProjectDict[xPrjStr]
		# -----------------------------------------
		pass

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		#if (self.XPrj != None):
		#	writer.WriteAttributeString('XPrj', self.XPrj.PyNS)
		# -----------------------------------------
		pass

	# ---------------------------------------------
	# BUILD
	# ---------------------------------------------
	def BuildTarget(self, xObj:WizObj=None):
		super().BuildTarget(xObj)
		# -----------------------------------------
		# X.Print ('Wiz.Module::BuildTarget ' + str(xObj))
		# -----------------------------------------
		pass

	# ---------------------------------------------
	# CREATE
	# ---------------------------------------------
	def SetMkoAttribs(self):
		super().SetMkoAttribs()
		# -------------------------------------
		self.S.MkoAttribs['mod'] = self

	def Source_Code(self, S):
		# -----------------------------------------
		for node in self.NodeList:
			node.Source_Code(S)

	def CreateIt(self):
		super().CreateIt()

	def SaveIt(self):
		super().SaveIt()

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, parent:Folder, copySource=False, mko:str=None) -> Module:
		# -----------------------------------------
		mod = Module(parent)
		mod.SetID(iD)
		parent.AddModule(mod)
		mod.CopySource = copySource
		mod.MkoFilePath = mko or mod.MkoFilePath
		# -----------------------------------------
		return mod

# =====================================================================
# Target
# =====================================================================
class Target(Folder):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.Modules:List[Module] = []
		self.ModuleDict:Dict[str, Module] = {}
		# -----------------------------------------
		self.Guid = None
		# -----------------------------------------
		self.DbgMsgs = False
		self.UseDirectDB = False
		self.UseCfg = False
		# -----------------------------------------
		self.PrivPrefix = '_'
		self.CtrlPrefix = 'Ctrl'
		self.ViewPrefix = 'UI'
		# -----------------------------------------
		self.PrivBegLC = True  # can't remember what these are?
		self.PubBegLC = False

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, parent:Folder) -> Target:
		# -----------------------------------------
		folder = Target(parent)
		folder.SetID(iD)
		parent.AddTarget(folder)
		# -----------------------------------------
		return folder

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def Tgt(self): 
		return self

	@property
	def XmlName(self): 
		return 'Target'
	
	@property
	def DefNamespace(self): 
		return self.ID

	@property
	def Namespace(self): 
		# -----------------------------------------
		if (self._namespace != None):
			return self._namespace
		else:
			return self.ID

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		# if (self.Prj != None):
		#	writer.WriteAttributeString('Project', self.Prj.ID)
		# -----------------------------------------
		writer.WriteAttributeNewLine()
		# -----------------------------------------
		if (self.Guid != None):
			writer.WriteAttributeString('Guid', str(self.Guid).upper())
		# -----------------------------------------
		writer.WriteAttributeNewLine()
		# -----------------------------------------
		if (self.DbgMsgs):
			writer.WriteAttributeString('DbgMsgs', 'Y')
		# -----------------------------------------
		if (self.PrivPrefix != '_'):
			writer.WriteAttributeString('PrivPrefix', self.PrivPrefix)
		# -----------------------------------------
		if (self.CtrlPrefix != 'Ctrl'):
			writer.WriteAttributeString('CtrlPrefix', self.CtrlPrefix)
		# -----------------------------------------
		if (self.ViewPrefix != 'UI'):
			writer.WriteAttributeString('ViewPrefix', self.ViewPrefix)
# =====================================================================
# Solution
# =====================================================================
class Solution(Base.Solution, Folder):

	def __init__(self, iD, rootPath=None, parent=None):
		super().__init__(parent)
		# -----------------------------------------
		self.ID = iD
		# -----------------------------------------
		if (self.Folder == None):
			self.DefRootPath = G.Temp + '/' + self.ID
		else:
			self.DefRootPath = self.Folder.FolderPath + '/' + self.ID
		# -----------------------------------------
		self.RootPath = rootPath
		if (self.RootPath == None):
			self.RootPath = self.DefRootPath
		# -----------------------------------------
		self.VSDefVer = G.VSVers.VS2008
		self.FWDefVer = G.FWVers.Net35
		# -----------------------------------------
		self.Modules:List[Module] = []
		self.ModuleDict:Dict[str, Module] = {}
		# -----------------------------------------
		self.Targets:List[Target] = []     # nodes
		self.TargetDict:Dict[str, Target] = {}

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD, rootPath=None, parent=None):
		# -----------------------------------------
		sln = Solution(iD, rootPath, parent)
		return sln

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def Sln(self): 
		# -----------------------------------------
		if (isinstance(self, Solution)):
			return self
		else:
			return self._sln

	@property
	def XmlName(self): 
		return 'Solution'

	@property
	def FolderPath(self): 
		# -----------------------------------------
		if (self.Folder == None):
			return self.RootPath
		else:
			return self.Folder.FolderPath + '/' + self.ID

	# ---------------------------------------------
	@property
	def XmlFolderPath(self): 
		# -----------------------------------------
		return self.FolderPath + '/__wiz__'

	@property
	def DefNamespace(self): 
		# -----------------------------------------
		if (self.Folder == None):
			return self.ID
		else:
			return self.Folder.DefNamespace + '.' + self.ID

	@property
	def Namespace(self): 
		# -----------------------------------------
		if (self._namespace != None):
			return self._namespace
		else:
			if (self.Folder == None):
				return self.ID
			else:
				return self.Folder.Namespace + '.' + self.ID

	@property
	def DottedPath(self): 
		# -----------------------------------------
		if (self.Parent == None):
			return self.ID
		else:
			return self.Folder.DottedPath + '.' + self.ID

	@property
	def XmlPath(self):
		# -----------------------------------------
		return self.FolderPath + '/' + self.ID + '.xml'

	# ---------------------------------------------
	# XML Doc
	# ---------------------------------------------
	def ReadXmlFile(self):
		# -----------------------------------------
		if (not os.path.exists(self.XmlPath)):
			Dbg.Warn('File does not exist: ' + self.XmlPath)
			return
		# -----------------------------------------
		tree = Et.ElementTree()
		tree.parse(self.XmlPath)
		root = tree.getroot()
		# -----------------------------------------
		self.ReadXML(root)

	def WriteXmlFile(self):
		# -----------------------------------------
		fldr = self.XmlFolderPath
		if (not os.path.exists(fldr)):
			os.makedirs(fldr)
		# -----------------------------------------
		stream = open(self.XmlPath, 'wt', encoding='utf-8-sig')
		writer = Xml.TextWriter(stream)
		self.WriteXML(writer)
		stream.close()

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('VS' in node.attrib):
			self.VSDefVer = G.VSVers[node.attrib['VS']]
		# -----------------------------------------
		if ('FW' in node.attrib):
			self.FWDefVer = G.FWVers[node.attrib['FW']]

	def XmlReadNode(self, node):
		# -----------------------------------------
		if (node.tag == 'Database'):
			# -------------------------------------
			import Db
			# -------------------------------------
			db = Db.Database(self)
			db.ReadXML(node)
			self.AddDatabase(db)
		# -----------------------------------------
		elif (node.tag == 'DbServer'):
			# -------------------------------------
			import Db
			# -------------------------------------
			dbSvr = Db.Server(self)
			dbSvr.ReadXML(node)
			self.AddDbServer(dbSvr)
		# -----------------------------------------
		# elif (node.tag == 'PrjFolder'):
		#	# -------------------------------------
		#	self.PrjFolder = X.PrjFolder(self)
		#	Dbg.LogIt('# = ReadXML Projects ==> in Solution')
		#	self.PrjFolder.ReadXML(node)
		# -----------------------------------------
		else:
			super().XmlReadNode(node)

	def XmlWriteNodes(self, writer):
		# -----------------------------------------
		# for db in self.Databases:
		#	db.WriteXML(writer)
		# -----------------------------------------
		# for dbSvr in self.DbServers:
		#	dbSvr.WriteXML(writer)
		# -----------------------------------------
		# if (self.PrjFolder != None):
		#	self.PrjFolder.WriteXML(writer)
		# -----------------------------------------
		super().XmlWriteNodes(writer)
