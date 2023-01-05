#
# Copyright James Ross (C) 2023
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
import Glb as G
#import X
#import Dbg

# =====================================================================
# Project
# =====================================================================
class Attribute(object):

	def __init__(self, name, value):
		super().__init__()
		# -----------------------------------------
		self.Name = name
		self.Value = value

	def ToXML(self):
		# -----------------------------------------
		return self.Name + '="' + self.Escape(str(self.Value)) + '"'

	def Escape(self, str):
		str = str.replace("&", "&amp;")
		str = str.replace("<", "&lt;")
		str = str.replace(">", "&gt;")
		str = str.replace("\"", "&quot;")
		return str

# ---------------------------------------------------------------------
class AttributeLine(object):

	def __init__(self):
		super().__init__()
		# -----------------------------------------
		self.Attributes = []

	def AppendAttribute(self, attribute):
		# -----------------------------------------
		self.Attributes.append(attribute)

	def ToXML(self):
		# -----------------------------------------
		lst = []
		for attrib in self.Attributes:
			lst.append(attrib.ToXML())
		# -----------------------------------------
		return ' '.join(lst)

# ---------------------------------------------------------------------
class Element(object):

	def __init__(self, tag, lvl):
		super().__init__()
		# -----------------------------------------
		self.Tag = tag
		self.Level = lvl
		self.HasNodes = False
		self.AttributeLines = []
		self.AppendNewLine()
		self.OpenTag = False

	def AppendAttribute(self, name, value):
		# -----------------------------------------
		self.AttributeLines[-1].AppendAttribute(Attribute(name, value))

	def AppendNewLine(self):
		# -----------------------------------------
		self.AttributeLines.append(AttributeLine())

	def WriteAttribs(self, stream):
		# -----------------------------------------
		if (len(self.AttributeLines) > 0):
			# -------------------------------------
			if (len(self.AttributeLines[0].Attributes) > 0):
				stream.write(' ' + self.AttributeLines[0].ToXML())
			# -------------------------------------
			for attribLine in self.AttributeLines[1:]:
				if (len(attribLine.Attributes) > 0):
					# -----------------------------
					tabs = ''
					for _ in range(self.Level+1):
						tabs += '\t'
					# -----------------------------
					stream.write('\n' + tabs + attribLine.ToXML())

# ---------------------------------------------------------------------
class TextWriter(object): ## IObject

	def __init__(self, stream):
		super().__init__()
		# -----------------------------------------
		# stream = open('output.txt','wt')
		# -----------------------------------------
		# stream = io.StringIO()
		# -----------------------------------------
		# xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		self.Stream = stream
		self.ElementStack = []

	def WriteStartElement(self, sTag, cmt=None):
		# -----------------------------------------
		if (len(self.ElementStack) > 0):
			if (self.ElementStack[-1].OpenTag):
				self.ElementStack[-1].WriteAttribs(self.Stream)
				self.Stream.write('>\n')
				self.ElementStack[-1].OpenTag = False
				self.ElementStack[-1].HasNodes = True
		# -----------------------------------------
		lvl = len(self.ElementStack)
		# -----------------------------------------
		element = Element(sTag, lvl)
		self.ElementStack.append(element)
		# -----------------------------------------
		tabstr = ''
		for _ in range(lvl):
			tabstr += '\t'
		# -----------------------------------------
		if (cmt != None):
			self.Stream.write(tabstr + '<!-- ' + cmt + ' -->\n')
		# -----------------------------------------
		self.Stream.write(tabstr + '<' + element.Tag)
		self.ElementStack[-1].OpenTag = True
	
	def WriteAttributeString(self, sAttr, val):
		# ----------------------------------------------------------
		self.ElementStack[-1].AppendAttribute(sAttr, val)

	def WriteAttributeNewLine(self):
		# ----------------------------------------------------------
		self.ElementStack[-1].AppendNewLine()

	def WriteEndElement(self):
		# -----------------------------------------
		if (len(self.ElementStack) > 0):
			element = self.ElementStack.pop()
			# -----------------------------------------
			if (element.HasNodes):
				# -------------------------------------
				tabstr = ''
				for _ in range(element.Level):
					tabstr += '\t'
				# -------------------------------------
				self.Stream.write(tabstr + '</' + element.Tag + '>\n')
			# -----------------------------------------
			else:
				element.WriteAttribs(self.Stream)
				self.Stream.write(' />\n')
			# -----------------------------------------
			element.OpenTag = False

# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	import datetime
	# -----------------------------------------------------------------
	f = open(G.WizLogPath, 'a')
	f.write('62815\tXmlWriter\t' + str(datetime.datetime.now()) + '\tXml\n')
	f.close()
	# -----------------------------------------------------------------
	stream = open('C:\\Temp\\tst_output.xml','wt')
	xmlout = TextWriter(stream)
	xmlout.WriteStartElement('Test')
	xmlout.WriteAttributeString('attrib', '1')
	xmlout.WriteAttributeNewLine()
	xmlout.WriteStartElement('Testing123')
	xmlout.WriteAttributeString('attrib', 'Ok')
	xmlout.WriteEndElement()
	xmlout.WriteStartElement('Testing456')
	xmlout.WriteAttributeString('attrib', 'it, works!')
	xmlout.WriteEndElement()
	xmlout.WriteStartElement('Testing789')
	xmlout.WriteAttributeString('ID', 'Testing789ID')
	xmlout.WriteStartElement('Testing0')
	xmlout.WriteStartElement('Testing1')
	xmlout.WriteAttributeString('Line1', 'YES')
	xmlout.WriteAttributeNewLine()
	xmlout.WriteAttributeString('Line2', 'YES')
	xmlout.WriteAttributeNewLine()
	xmlout.WriteAttributeString('Line3', 'YES')
	xmlout.WriteAttributeString('Line4', 'Maybe!')
	xmlout.WriteStartElement('Testing2', 'ahh, yes Worky, Worky!')
	xmlout.WriteAttributeString('ID', 'Testing2ID')
	xmlout.WriteAttributeString('Easy', 'YES')
	xmlout.WriteAttributeNewLine()
	xmlout.WriteAttributeNewLine()
	xmlout.WriteAttributeString('DoesIT', 'YES')
	xmlout.WriteEndElement()
	xmlout.WriteEndElement()
	xmlout.WriteEndElement()
	xmlout.WriteEndElement()
	xmlout.WriteEndElement()
	stream.close()
	# -----------------------------------------------------------------
	# p_rint ('OK!')