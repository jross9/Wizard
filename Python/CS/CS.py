from __future__ import annotations

import uuid

import Glb as G
import Base
import Dbg
import Wiz
# import VS

# =====================================================================
# Source
# =====================================================================
class Source(Base.Source):

	def Code(self, tabs, str=None):
		# -----------------------------------------
		tstr = str
		if (str == None):
			tstr = tabs
		# -----------------------------------------
		if (tstr == '}'):
			if (self.C[-1] == ''):
				self.C.pop()
		# -----------------------------------------
		super().Code(tabs, str)
		# -----------------------------------------
		if (tstr[-1] == '{'):  # if took out add check below in ClassHeaderLine
			self.NoEmptyLine = True

	def ClassHeaderLine(self, cls):
		# -----------------------------------------
		if (not self.NoEmptyLine): #if (!C[C.Count - 1].EndsWith("{") && !_noEmptyLine)
			self.C.append('')
		# -----------------------------------------
		c = '/'; line = ''; maxl = 79; ex = 0
		# -----------------------------------------
		label = cls.TypeName
		if (cls.AddNS != None):
			label = cls.AddNS + '.' + cls.TypeName
		# -----------------------------------------
		for _ in range(self.TabLevel):
			line += '\t'
			ex += 4
		# -----------------------------------------
		ix = 0
		# -----------------------------------------
		if (cls.ScopeType == G.ScopeType.Public):
			ix += 7; ex += 7 # 'public '
		# -----------------------------------------
		if (cls.IsStatic):
			ix += 7; ex += 7 # 'static '
		# -----------------------------------------
		if (cls.IsPartial):
			ix += 8; ex += 8 # 'partial '
		# -----------------------------------------
		if (cls.IsInterface):
			ix += 9; ex += 9 # 'interface'
		else:
			ix += 5; ex += 5 # 'class'
		# -----------------------------------------
		for _ in range(ix): line += c
		# -----------------------------------------
		line += ' ' + label + ' '; ex += 2
		# -----------------------------------------
		for _ in range(maxl - ex - len(label)): line += c
		# -----------------------------------------
		self.C.append(line)
		self.C.append('')
		self.NoEmptyLine = True

	def DividerLine(self, txt):
		# -----------------------------------------
		if (not self.NoEmptyLine):
			self.C.append('')
		# -----------------------------------------
		c = '='; line = ''; maxl = 79; ex = 0
		# -----------------------------------------
		for _ in range(self.TabLevel):
			line += '\t'
			ex += 4
		# -----------------------------------------
		line += '// '; ex += 3
		# -----------------------------------------
		ix = 11; ex += 11
		# -----------------------------------------
		for _ in range(ix): line += c
		# -----------------------------------------
		line += ' ' + txt + ' '; ex += 2
		# -----------------------------------------
		for _ in range(maxl - ex - len(txt)): line += c
		# -----------------------------------------
		self.C.append(line)
		self.C.append('')
		self.NoEmptyLine = True

# =====================================================================
# AstNode
# =====================================================================
class AstNode(Wiz.AstNode):

	def __init__(self, parent):
		super().__init__(parent)

	# ---------------------------------------------
	# CREATE
	# ---------------------------------------------
	def Source_Code(self, CS):
		# -----------------------------------------
		CS.Code('// CS.AstNode::Source_Code: ' + str(self))
		# -----------------------------------------
		for node in self.NodeList:
			node.Source_Code(CS)

# ---------------------------------------------------------------------
class AstBlock(Wiz.AstBlock, AstNode):

	def __init__(self, parent):
		super().__init__(parent)

	# ---------------------------------------------
	# NEW
	# ---------------------------------------------

# =====================================================================
# Comments
# =====================================================================
class Comment(Wiz.Comment, AstNode):

	def __init__(self, parent):
		super().__init__(parent)

# ---------------------------------------------------------------------
class LineComment(Wiz.LineComment, Comment):

	def __init__(self, parent):
		super().__init__(parent)

	# ---------------------------------------------
	# CREATE
	# ---------------------------------------------
	def Source_Code(self, CS):
		# -----------------------------------------
		CS.Code('// ' + str(self.Comment))
		# -----------------------------------------
		if (self.EmptyLine):
			CS.Blank()

# ---------------------------------------------------------------------
class BlockComment(Wiz.BlockComment, Comment):

	def __init__(self, parent):
		super().__init__(parent)

# =====================================================================
# Target
# =====================================================================
class Target(Wiz.Target):

	def __init__(self, parent:Wiz.Folder):
		super().__init__(parent)

	# ---------------------------------------------
	# static XmlReadNodes
	# ---------------------------------------------
	@staticmethod
	def XmlReadNodes(node, parent):
		# -----------------------------------------
		if (node.tag == 'CSharp.Module'):
			# -------------------------------------
			#mod = Module.MAKE(node.attrib['ID'], parent)
			#mod.ReadXML(node)
			# -------------------------------------
			pass
		# -----------------------------------------
		elif (node.tag == 'CSharp.AssemblyInfo'):
			# -------------------------------------
			#mod = AssemblyInfoModule.MAKE(node.attrib['ID'], parent)
			#mod.ReadXML(node)
			# -------------------------------------
			pass
		# -----------------------------------------
		elif (node.tag == 'CSharp.Lib'):
			# -------------------------------------
			import CS.Lib
			# -------------------------------------
			tgt = CS.Lib.Target.MAKE(node.attrib['ID'], parent)
			tgt.ReadXML(node)
		# -----------------------------------------
		elif (node.tag == 'CSharp.WinForm'):
			# -------------------------------------
			#import CS.WF
			# -------------------------------------
			#tgt = CS.WF.Target.MAKE(node.attrib['ID'], parent)
			#tgt.ReadXML(node)
			# -------------------------------------
			pass
		# -----------------------------------------
		elif (node.tag == 'CSharp.WinForm'):
			# -------------------------------------
			#import CS.WF
			# -------------------------------------
			#tgt = CS.WF.Target.MAKE(node.attrib['ID'], parent)
			#tgt.ReadXML(node)
			# -------------------------------------
			pass
		# -----------------------------------------
		else:
			raise Base.UnknowNodeException('Bad NODE Tag [' + node.tag + ']')

