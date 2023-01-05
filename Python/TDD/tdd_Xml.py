#
# Copyright James Ross (C) 2023
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
#!/usr/bin/python3

#import datetime
import unittest
#import collections

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import io

import Glb as G
#import Base
import Xml
import Dbg
import TDD.UTLib as UT

# ---------------------------------------------------------------------
# 
# ---------------------------------------------------------------------
class Attribute_Tests(unittest.TestCase):

	def test_Constructor_Defaults(self):
		# -----------------------------------------
		attr = Xml.Attribute('Attribute', 'OK')
		# -----------------------------------------
		self.assertEqual(attr.Name, 'Attribute')
		self.assertEqual(attr.Value, 'OK')

	def test_ToXML(self):
		# -----------------------------------------
		attr = Xml.Attribute('Attribute', 'OK')
		# -----------------------------------------
		self.assertEqual(attr.ToXML(), 'Attribute="OK"')

class AttributeLine_Tests(unittest.TestCase):

	def test_Constructor_Defaults(self):
		# -----------------------------------------
		attr_line = Xml.AttributeLine()
		# -----------------------------------------
		self.assertEqual(attr_line.Attributes, [])
		self.assertEqual(attr_line.ToXML(), '')

	def test_AppendAttributes(self):
		# -----------------------------------------
		attr_line = Xml.AttributeLine()
		attr_line.AppendAttribute(Xml.Attribute('Attribute', 'OK'))
		# -----------------------------------------
		self.assertEqual(len(attr_line.Attributes), 1)
		# -----------------------------------------
		attr_line.AppendAttribute(Xml.Attribute('Attribute2', 'OK2'))
		# -----------------------------------------
		self.assertEqual(len(attr_line.Attributes), 2)
		self.assertEqual(attr_line.ToXML(), 'Attribute="OK" Attribute2="OK2"')

class Element_Tests(unittest.TestCase):

	def test_Constructor_Defaults(self):
		# -----------------------------------------
		element = Xml.Element('Tag', 0)
		# -----------------------------------------
		self.assertEqual(element.Tag, 'Tag')
		self.assertEqual(element.Level, 0)
		self.assertEqual(element.HasNodes, False)
		self.assertEqual(len(element.AttributeLines), 1)
		self.assertEqual(element.AttributeLines[0].Attributes, [])
		self.assertEqual(element.OpenTag, False)
		# -----------------------------------------
		element.AttributeLines[0].AppendAttribute(Xml.Attribute('Attribute1', 'OK1'))
		element.AttributeLines[0].AppendAttribute(Xml.Attribute('Attribute2', 'OK2'))
		# -----------------------------------------
		stream = io.StringIO()
		element.WriteAttribs(stream)
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), ' Attribute1="OK1" Attribute2="OK2"')

class TextWriter_Tests(unittest.TestCase):

	def test_Constructor_Defaults(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		self.assertEqual(xmlout.Stream, stream)
		self.assertEqual(xmlout.ElementStack, [])
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), '')

	def test_SimpleTag(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), '<Test />\n')

	def test_SimpleTagAndAttribute(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute', 'OK')
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), '<Test Attribute="OK" />\n')

	def test_SimpleTagAndAttribute2(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute1', 'OK1')
		xmlout.WriteAttributeString('Attribute2', 'OK2')
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), '<Test Attribute1="OK1" Attribute2="OK2" />\n')

	def test_ElementWithNode(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute', 'OK')
		xmlout.WriteStartElement('Node')
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Test Attribute="OK">', 
			'\t<Node />',
			'</Test>']))

	def test_ElementWith2Nodes(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute', 'OK')
		xmlout.WriteStartElement('Node')
		xmlout.WriteEndElement()
		xmlout.WriteStartElement('Node')
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Test Attribute="OK">', 
			'\t<Node />',
			'\t<Node />',
			'</Test>']))

	def test_ElementWithSubNodes(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute', 'OK')
		xmlout.WriteStartElement('Node')
		xmlout.WriteStartElement('Node')
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Test Attribute="OK">', 
			'\t<Node>',
			'\t\t<Node />',
			'\t</Node>',
			'</Test>']))

	def test_ElementsWitEmptyMultiLine(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), '<Test />\n')

	def test_ElementWithMultiLine(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteAttributeString('Attribute', 'OK')
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Test', 
			'\tAttribute="OK" />']))

	def test_ElementWithMultiLine2(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute1', 'OK1')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteAttributeString('Attribute2', 'OK2')
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Test Attribute1="OK1"', 
			'\tAttribute2="OK2" />']))

	def test_ElementsWithMultiLine(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute', 'OK')
		xmlout.WriteStartElement('Node')
		xmlout.WriteAttributeString('Attribute2', 'OK2')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteAttributeString('Attribute2b', 'OK2b')
		xmlout.WriteStartElement('Node')
		xmlout.WriteAttributeString('Attribute3', 'OK3')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteAttributeString('Attribute3b', 'OK3b')
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Test Attribute="OK">', 
			'\t<Node Attribute2="OK2"',
			'\t\tAttribute2b="OK2b">',
			'\t\t<Node Attribute3="OK3"',
			'\t\t\tAttribute3b="OK3b" />',
			'\t</Node>',
			'</Test>']))

	def test_ElementsWithMultiLine2(self):
		# -----------------------------------------
		stream = io.StringIO()
		xmlout = Xml.TextWriter(stream)
		# -----------------------------------------
		xmlout.WriteStartElement('Test')
		xmlout.WriteAttributeString('Attribute1', 'OK1')
		xmlout.WriteAttributeString('Attribute1b', 'OK1b')
		xmlout.WriteStartElement('Node')
		xmlout.WriteAttributeString('Attribute2', 'OK2')
		xmlout.WriteAttributeString('Attribute2b', 'OK2b')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteAttributeString('Attribute2c', 'OK2c')
		xmlout.WriteAttributeString('Attribute2d', 'OK2d')
		xmlout.WriteStartElement('Node')
		xmlout.WriteAttributeString('Attribute3', 'OK3')
		xmlout.WriteAttributeString('Attribute3b', 'OK3b')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteAttributeString('Attribute3c', 'OK3c')
		xmlout.WriteAttributeString('Attribute3d', 'OK3d')
		xmlout.WriteStartElement('Node')
		xmlout.WriteAttributeString('Attribute4', 'OK4')
		xmlout.WriteAttributeString('Attribute4b', 'OK4b')
		xmlout.WriteAttributeNewLine()
		xmlout.WriteAttributeString('Attribute4c', 'OK4c')
		xmlout.WriteStartElement('Node')
		xmlout.WriteAttributeString('Attribute5', 'OK5')
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		xmlout.WriteEndElement()
		# -----------------------------------------
		self.assertEqual(stream.getvalue(), UT.List2Str([
			'<Test Attribute1="OK1" Attribute1b="OK1b">', 
			'\t<Node Attribute2="OK2" Attribute2b="OK2b"',
			'\t\tAttribute2c="OK2c" Attribute2d="OK2d">',
			'\t\t<Node Attribute3="OK3" Attribute3b="OK3b"',
			'\t\t\tAttribute3c="OK3c" Attribute3d="OK3d">',
			'\t\t\t<Node Attribute4="OK4" Attribute4b="OK4b"',
			'\t\t\t\tAttribute4c="OK4c">',
			'\t\t\t\t<Node Attribute5="OK5" />',
			'\t\t\t</Node>',
			'\t\t</Node>',
			'\t</Node>',
			'</Test>']))

# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	G.LogCount('TDD_Xml', 'Unit (Python)')
	# -----------------------------------------------------------------
	Dbg.LogOff = True
	# -----------------------------------------------------------------
	unittest.main()
