#
# Copyright James Ross (C) 2022
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
#!/usr/bin/python3

import unittest

import xml.etree.ElementTree as Et

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Glb as G
import Dbg
import TDD.UTLib as UT

import Base

# =====================================================================
# Source Tests
# =====================================================================
class Source_Tests(unittest.TestCase):

	def test_Code_Inserts_A_Line(self):
		# -----------------------------------------
		src = Base.Source()
		src.Code('Testing123')
		self.assertEqual(src.ToStr(), 'Testing123')

	def test_Code_Inserts_Multiple_Line(self):
		# -----------------------------------------
		src = Base.Source()
		src.Code('Testing123')
		src.Code('Testing456')
		src.Code('Testing789')
		self.assertEqual(src.ToStr(), UT.List2StrSrc(src, [
			'Testing123', 
			'Testing456',
			'Testing789']))

	def test_Code_Inserts_Multiple_Line_Unix(self):
		# -----------------------------------------
		src = Base.Source()
		src.UNIX = True
		src.Code('Testing123')
		src.Code('Testing456')
		src.Code('Testing789')
		self.assertEqual(src.ToStr(), UT.List2StrSrc(src, [
			'Testing123', 
			'Testing456',
			'Testing789']))

	def test_Code_Inserts_Blank(self):
		# -----------------------------------------
		src = Base.Source()
		src.Code('Testing123')
		src.Blank()
		src.Code('Testing456')
		self.assertEqual(src.ToStr(), UT.List2StrSrc(src, [
			'Testing123', 
			'',
			'Testing456']))

	def test_Code_Inserts_Only_One_Contiguous_Blank(self):
		# -----------------------------------------
		src = Base.Source()
		src.Code('Testing123')
		src.Blank()
		src.Blank()
		src.Code('Testing456')
		src.Blank()
		src.Blank()
		src.Blank()
		src.Code('Testing789')
		self.assertEqual(src.ToStr(), UT.List2StrSrc(src, [
			'Testing123', 
			'',
			'Testing456',
			'',
			'Testing789']))

# =====================================================================
# BaseObj
# =====================================================================
class Object_Tests(unittest.TestCase):

	def test_Object_Has_No_Parent_Exception(self):
		# -----------------------------------------
		with self.assertRaises(Base.NoParentException):
			# -------------------------------------
			obj = Base.BaseObj(None)

	def test_Object_Has_No_XmlName_Func_Exception(self):
		# -----------------------------------------
		with self.assertRaises(Base.NoXmlNameFunc):
			# -------------------------------------
			sln = Base.Solution.MAKE()
			obj = Base.BaseObj(sln)
			# -------------------------------------
			obj.XmlName

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Base.Solution.MAKE()
		obj = Base.BaseObj(sln)
		# -----------------------------------------
		self.assertEqual(obj.Parent, sln)
		self.assertEqual(obj.Sln, sln)
		self.assertEqual(obj.Parent, obj.Sln)

	def test_Xml_Unknown_Node_Exception(self):
		# -----------------------------------------
		sln = Base.Solution.MAKE()
		obj = Base.BaseObj(sln)
		# -----------------------------------------
		node = Et.fromstring('''
			<BaseObj>
				<UnknownNode />
			</BaseObj>
		''')
		# -----------------------------------------
		with self.assertRaises(Base.UnknowNodeException):
			sln.ReadXML(node)

# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	G.LogCount('tdd_Base', 'Unit (Python)')
	# -----------------------------------------------------------------
	Dbg.LogOff = True
	# -----------------------------------------------------------------
	unittest.main()
