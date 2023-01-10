#!/usr/bin/python3

import unittest
# import xml.etree.ElementTree as Et

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import Glb as G
import Dbg

import Db

#import X
import Wiz

# =====================================================================
# 
# =====================================================================
class Database_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		db = Db.Database.MAKE('Database', sln)
		# -----------------------------------------
		self.assertEqual(db.ID, 'Database')

# =====================================================================
# 
# =====================================================================
class Table_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		db = Db.Database.MAKE('Database', sln)
		tbl = Db.Table.MAKE('Table', db)
		# -----------------------------------------
		self.assertEqual(tbl.ID, 'Table')

# =====================================================================
# 
# =====================================================================
class Field_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		db = Db.Database.MAKE('Database', sln)
		tbl = Db.Table.MAKE('Table', db)
		fld = Db.Field.MAKE('Field', tbl)
		# -----------------------------------------
		self.assertEqual(fld.ID, 'Field')

# =====================================================================
# 
# =====================================================================
class Db_Tests(unittest.TestCase):

	def test_Factory_Field(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		db = Db.Database.MAKE('Database', sln)
		tbl = Db.Table.MAKE('Table', db)
		fld = Db.Field.MAKE('Field', tbl)
		# -----------------------------------------
		self.assertEqual(fld.ID, 'Field')
 
# =====================================================================
# 
# =====================================================================
class CoCoDb_Tests(unittest.TestCase):

	def test_ConstructorDefaults(self):
		# -----------------------------------------
		sln = Wiz.Solution.MAKE('Solution')
		self.assertIsNotNone(sln)
		self.assertEqual(0, len(sln.Databases))

		db = Db.Factory.Database.Create('CoCoDb', 'ccdb', sln)
		self.assertEqual(1, len(sln.Databases))

		# tbl = Db.Factory.Table.Create('Software', db)
		# tbl.Abbr = 'Sw'
		# Db.Factory.Field.Create('Fld1', tbl)
		# Db.Factory.Field.Create('Fld2', tbl)
		# -----------------------------------------


# =====================================================================
# 
# =====================================================================
if __name__ == '__main__':
	# -----------------------------------------------------------------
	G.LogCount('tdd_Db', 'Unit (Python)')
	# -----------------------------------------------------------------
	Dbg.LogOff = True
	# -----------------------------------------------------------------
	unittest.main()
