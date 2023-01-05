#
# Copyright James Ross (C) 2023
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
from __future__ import annotations

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
	def Tgt(self): return self._tgt

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
# Node / File / Folder
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

# =====================================================================
# Folder
# =====================================================================
class Folder(FSNode):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.IsVirtual = False
		self.UseParentNS = False

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self): return 'Folder'

	@property
	def IsFolder(self): return True

	@property
	def FolderPath(self): 
		# -----------------------------------------
		if (self.IsVirtual):
			return self.Folder.FolderPath
		else:
			return self.Folder.FolderPath + '/' + self.ID

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


# =====================================================================
# Target
# =====================================================================
class Target(Folder):

	def __init__(self, parent):
		super().__init__(parent)

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

