#
# Copyright James Ross (C) 2022
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
import codecs

import Glb as G
import Dbg

# =====================================================================
# BaseObj
# =====================================================================
class BaseObj(object):

	def __init__(self, parent):
		# -----------------------------------------
		self.Parent = None
		self._sln = None
		# -----------------------------------------
		if (parent != None): # parent == None
			# -------------------------------------
			self.Parent = parent
			# -----------------------------------------
			if (isinstance(parent, Solution)):
				self._sln = parent
			else:
				self._sln = parent.Sln
		# -----------------------------------------
		else:
			if (not isinstance(self, Solution)):
				raise NoParentException('NULL Parent for: ' + str(self))

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def Sln(self): 
		return self._sln

	@property
	def XmlName(self):
		# -----------------------------------------
		raise NoXmlNameFunc('No XmlName for: ' + str(self))

	# ---------------------------------------------
	# XML Methods
	# ---------------------------------------------
	def ReadXML(self, node):
		# -----------------------------------------
		self.XmlReadAttributes(node)
		# -----------------------------------------
		for subnode in node:
			self.XmlReadNode(subnode);

	def WriteXML(self, writer):
		# -----------------------------------------
		writer.WriteStartElement(self.XmlName)
		self.XmlWriteAttributes(writer)
		self.XmlWriteNodes(writer)
		writer.WriteEndElement()

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		# -----------------------------------------
		pass

	def XmlReadNode(self, node):
		# -----------------------------------------
		raise UnknowNodeException('Bad NODE Tag [' + node.tag + ']')

	def XmlWriteAttributes(self, writer):
		# -----------------------------------------
		pass

	def XmlWriteNodes(self, writer):
		# -----------------------------------------
		pass

	# ---------------------------------------------
	# Initialize
	# ---------------------------------------------
	def InitializeObj(self):
		# -----------------------------------------
		pass

# ---------------------------------------------------------------------
class IDObj(BaseObj):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.ID = None

	# ---------------------------------------------
	# METHODS
	# ---------------------------------------------
	def SetID(self, iD):
		# -----------------------------------------
		self.ID = iD

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('ID' in node.attrib):
			self.ID = node.attrib['ID'] 

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		if (self.ID != None):
			writer.WriteAttributeString('ID', self.ID)

# ---------------------------------------------------------------------
class NamedObj(IDObj):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.Name = None
		# -----------------------------------------
		self.Abbr = None
		self.Plural = None
		# -----------------------------------------
		self.Title = None
		self.Desc = None

	# ---------------------------------------------
	def SetID(self, iD):
		super().SetID(iD)
		# -----------------------------------------
		self.Name = iD
		# -----------------------------------------
		self.Abbr = iD
		self.Plural = iD + 's'

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('Name' in node.attrib):
			self.Name = node.attrib['Name'] 
		# -----------------------------------------
		if ('Abbr' in node.attrib):
			self.Abbr = node.attrib['Abbr'] 
		# -----------------------------------------
		if ('Plural' in node.attrib):
			self.Plural = node.attrib['Plural'] 
		# -----------------------------------------
		if ('Title' in node.attrib):
			self.Title = node.attrib['Title'] 
		# -----------------------------------------
		if ('Desc' in node.attrib):
			self.Desc = node.attrib['Desc'] 

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		if (self.Name != self.ID):
			writer.WriteAttributeString('Name', self.Name)
		# -----------------------------------------
		if (self.Abbr != self.ID):
			writer.WriteAttributeString('Abbr', self.Abbr)
		# -----------------------------------------
		if (self.Plural != self.ID + 's'):
			writer.WriteAttributeString('Plural', self.Plural)
		# -----------------------------------------
		if (self.Title != None):
			writer.WriteAttributeString('Title', self.Title)
		# -----------------------------------------
		if (self.Desc != None):
			writer.WriteAttributeString('Desc', self.Desc)

# =====================================================================
# Solution
# =====================================================================
class Solution(BaseObj):

	def __init__(self, parent):
		super().__init__(parent)

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE():
		# -----------------------------------------
		sln = Solution(None)
		return sln

# =====================================================================
# 
# =====================================================================
class NoParentException(Exception):
	pass

# ---------------------------------------------------------------------
class UnknowNodeException(Exception):
	pass

# ---------------------------------------------------------------------
class NoXmlNameFunc(Exception):
	pass

# =====================================================================
# Source
# =====================================================================
class Source(object):

	def __init__(self):
		# -----------------------------------------
		self.UTF8 = False
		self.UNIX = False
		self.BOM = False
		self.C = []
		self.TabLevel = 0
		self.NoEmptyLine = False
		# -----------------------------------------
		self.MkoTemplate = None
		self.MkoAttribs = {}

	def IsEmpty(self):
		# -----------------------------------------
		return len(self.C) == 0

	def Blank(self):
		# -----------------------------------------
		if (not self.NoEmptyLine):
			self.C.append('')
			self.NoEmptyLine = True

	def Code(self, tabs, str=None):
		# -----------------------------------------
		tstr = ''
		if (str != None):
			# -------------------------------------
			t = int(len(tabs)/3) + self.TabLevel
			for x in range(t):
				tstr += '\t'
			self.C.append(tstr + str)
		else:
			# -------------------------------------
			for x in range(self.TabLevel):
				tstr += '\t'
			self.C.append(tstr + tabs)
		# -----------------------------------------
		self.NoEmptyLine = False

	def AppendStr(self, str):
		# -----------------------------------------
		if (not self.IsEmpty()):
			self.C[-1] += str
		else:
			self.C.append(str)

	def AppendSrc(self, S):
		# -----------------------------------------
		for ln in S.C:
			self.C.append(ln) # JAR_NOTE: beed to check for EmptyLine?
		# -----------------------------------------
		if (self.C[-1] == ''):
			self.NoEmptyLine = True
		else:
			self.NoEmptyLine = False

	def _SetEmptyLineFlag(self):
		pass

	def Save(self, path):
		# -----------------------------------------
		if (self.MkoTemplate != None):
			# -------------------------------------
			sr = self.MkoTemplate.render(**self.MkoAttribs)
			utf = 'utf-8'
			if (self.BOM):
				utf = 'utf-8-sig' # w/ BOM
			f = codecs.open(path, 'w', utf)  
			f.write(sr)
			f.close()
			return
		# -----------------------------------------
		if (self.UTF8):
			if (self.BOM):
				f = codecs.open(path, 'w', 'utf-8-sig')  # w/ BOM
			else:
				f = codecs.open(path, 'w', 'utf-8') # w/o BOM
			for ln in self.C:
				if (self.UNIX):
					f.write(ln + '\n')
				else:
					f.write(ln + '\r\n')
		else:
			f = open(path, 'wb')
			for ln in self.C:
				if (self.UNIX):
					f.write(bytes(ln + '\n', 'UTF-8'))
				else:
					f.write(bytes(ln + '\r\n', 'UTF-8'))
		f.close()

	def RemoveComma(self): 
		# -----------------------------------------
		ln = self.C.pop()
		self.C.append(ln[:-1])

	def TabInc(self):
		# -----------------------------------------
		self.TabLevel += 1

	def TabDec(self):
		# -----------------------------------------
		if (self.TabLevel > 0):
			self.TabLevel -= 1

	def TabIncN(self, n):
		# -----------------------------------------
		self.TabLevel += n

	def TabDecN(self, n):
		# -----------------------------------------
		self.TabLevel -= n
		# -----------------------------------------
		if (self.TabLevel < 0):
			self.TabLevel = 0

	def ToStr(self):
		# -----------------------------------------
		if (self.MkoTemplate != None):
			return self.MkoTemplate.render(**self.MkoAttribs)
		# -----------------------------------------
		if (self.UNIX):
			return '\n'.join(self.C)
		else:
			return '\r\n'.join(self.C)

# ---------------------------------------------------------------------
class XmlSource(Source):

	pass

# ---------------------------------------------------------------------
class MakoSource(object):

	def __init__(self, context):
		# -----------------------------------------
		self._ctx = context 
		self.TabLevel = 0

	def Blank(self):
		# -----------------------------------------
		pass

	def Code(self, tabs, str=None):
		# -----------------------------------------
		tstr = ''
		if (str != None):
			# -------------------------------------
			t = int(len(tabs)/3) + self.TabLevel
			for x in range(t):
				tstr += '\t'
			self._ctx.write(tstr + str + '\r\n')
		else:
			# -------------------------------------
			for x in range(self.TabLevel):
				tstr += '\t'
			self._ctx.write(tstr + tabs + '\r\n')
		# -----------------------------------------
		self.NoEmptyLine = False

	def AppendStr(self, str):
		# -----------------------------------------
		self._ctx.write(str)

	def AppendSrc(self, S):
		# -----------------------------------------
		raise Exception('xxx NOT SUPPORTED')

	def RemoveComma(self): 
		# -----------------------------------------
		raise Exception('xxx NOT SUPPORTED')

	def TabInc(self, n=1):
		# -----------------------------------------
		self.TabLevel += n

	def TabDec(self, n=1):
		# -----------------------------------------
		self.TabLevel -= n
		if (self.TabLevel < 0):
			self.TabLevel = 0

	def ToStr(self):
		# -----------------------------------------
		raise Exception('ToStr NOT SUPPORTED')

	def ClassHeaderLine(self, str):
		# -----------------------------------------
		remaining = '/' * (80-len(str)-19)
		self._ctx.write(str + ' ' + remaining)
