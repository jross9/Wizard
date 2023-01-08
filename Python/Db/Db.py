from __future__ import annotations

import Glb as G
import Base
import Wiz

# =====================================================================
# DbObj
# =====================================================================
class DbObj(Base.NamedObj):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.Db = None
		# -----------------------------------------
		if (isinstance(parent, Database)):
			self.Db = parent
		elif (isinstance(parent, DbObj)):
			self.Db = parent.Db

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)

# =====================================================================
# Database
# =====================================================================
class Database(DbObj):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		self.Tables = []
		self.TableDict = {}

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self):
		# -----------------------------------------
		return 'Database'

	# ---------------------------------------------
	# METHODS
	# ---------------------------------------------
	def AddTable(self, tbl):
		self.Tables.append(tbl)
		G.SetKey(tbl.ID, tbl, self.TableDict)

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadNode(self, node):
		# -----------------------------------------
		if (node.tag == 'Table'):
			tbl = Table(self)
			tbl.ReadXML(node)
			self.AddTable(tbl)
		# -----------------------------------------
		else:
			raise Base.UnknowNodeException('Bad NODE Tag [' + node.tag + ']')

	def XmlWriteNodes(self, writer):
		# -----------------------------------------
		for tbl in self.Tables:
			tbl.WriteXML(writer)
		# -----------------------------------------
		super().XmlWriteNodes(writer)

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, sln:Wiz.Solution) -> Database:
		# -----------------------------------------
		db = Database(sln)
		db.SetID(iD)
		sln.AddDatabase(db)
		# -----------------------------------------
		return db

# =====================================================================
# Table
# =====================================================================
class Table(DbObj):

	def __init__(self, db):
		super().__init__(db)
		# -----------------------------------------
		self.Fields = []
		self.FieldDict = {}

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self):
		# -----------------------------------------
		return 'Table'

	# ---------------------------------------------
	# METHODS
	# ---------------------------------------------
	def AddField(self, fld):
		self.Fields.append(fld)
		G.SetKey(fld.ID, fld, self.FieldDict)

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadNode(self, node):
		# -----------------------------------------
		if (node.tag == 'Field'):
			fld = Field(self)
			fld.ReadXML(node)
			self.AddField(fld)
		# -----------------------------------------
		else:
			raise Base.UnknowNodeException('Bad NODE Tag [' + node.tag + ']')

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		#if (self.Abbr != self.ID):
		#	writer.WriteAttributeString('Abbr', self.Abbr)

	def XmlWriteNodes(self, writer):
		# -----------------------------------------
		for fld in self.Fields:
			fld.WriteXML(writer)
		# -----------------------------------------
		super().XmlWriteNodes(writer)

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, db:Database) -> Table:
		# -----------------------------------------
		tbl = Table(db)
		tbl.SetID(iD)
		db.AddTable(tbl)
		# -----------------------------------------
		return tbl

# =====================================================================
# Field
# =====================================================================
class Field(DbObj):

	def __init__(self, tbl):
		super().__init__(tbl)
		# -----------------------------------------
		self.Table = tbl
		# -----------------------------------------
		# --- XML values, purely database  --------
		# -----------------------------------------
		self.DbType = G.DbType.String
		# -----------------------------------------
		self.IsPK = False
		self.IsAuto = False
		self.MaxLength = 64    # for type strings / binary ??
		self.Required = False
		self.DefValue = None
		self.Ordinal = 0
		# -----------------------------------------
		# --- XML values -- Wizard Specials -------
		# -----------------------------------------
		self.ClientName = None
		self.SqlName = None
		# -----------------------------------------
		self.NoApostrophe = False # for type strings
		# -----------------------------------------
		self.EnumType = None
		self.Enumerations = []
		self.ValDict = {}
		# -----------------------------------------
		# --- Code GEN Helpers / Field Names  -----
		# -----------------------------------------
		self.PerlVar = None
		self.PerlSQLVar = None
		self.CSharpLocalVar = None
		self.CSharpType = None
		self.CSharpConvertTo = None

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self):
		# -----------------------------------------
		return 'Field'

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('Req' in node.attrib):
			self.Required = True
		# -----------------------------------------
		if ('Type' in node.attrib):
			self.DbType = G.DbType[node.attrib['Type']]
		# -----------------------------------------
		if ('PK' in node.attrib):
			self.IsPK = True
			self.Table.PKFld = self
		# -----------------------------------------
		if ('Auto' in node.attrib):
			self.IsAuto = True
		# -----------------------------------------
		if ('Len' in node.attrib):
			self.MaxLength = int(node.attrib['Len'])

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		if (self.Required):
			writer.WriteAttributeString('Req', 'Y')
		# -----------------------------------------
		writer.WriteAttributeString('Type', self.DbType.name)
		# -----------------------------------------
		if (self.IsPK):
			writer.WriteAttributeString('PK', 'Y')
		# -----------------------------------------
		if (self.IsAuto):
			writer.WriteAttributeString('Auto', 'Y')
		# -----------------------------------------
		if (self.MaxLength != 64):
			writer.WriteAttributeString('Len', str(self.MaxLength))

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, tbl:Table) -> Field:
		# -----------------------------------------
		fld = Field(tbl)
		fld.SetID(iD)
		tbl.AddField(fld)
		# -----------------------------------------
		return fld

# =====================================================================
# DbServer
# =====================================================================
class Server(Base.BaseObj):

	def __init__(self, parent):
		super().__init__(parent)
		# -----------------------------------------
		# None, Access, SQLite, SQLServer, Oracle, MySQL, PostgreSQL
		self.DbSvrType = G.DbSvrType.Access # DbSvrType.xxx
		# SQLCE, SQLServer, SQLExpress, LocalDb
		self.SQLSvrType = G.SQLSvrType.SQLCE # SQLServerTypes.xxx
		# -----------------------------------------
		self.Db = None

	# ---------------------------------------------
	# PROPERTIES
	# ---------------------------------------------
	@property
	def XmlName(self):
		# -----------------------------------------
		return 'DbServer'

	# ---------------------------------------------
	# XML Overrides
	# ---------------------------------------------
	def XmlReadAttributes(self, node):
		super().XmlReadAttributes(node)
		# -----------------------------------------
		if ('Type' in node.attrib):
			self.DbSvrType = G.DbSvrType[node.attrib['Type']]
		# -----------------------------------------
		if ('SQLType' in node.attrib):
			self.SQLSvrType = G.SQLSvrType[node.attrib['SQLType']]

	def XmlWriteAttributes(self, writer):
		super().XmlWriteAttributes(writer)
		# -----------------------------------------
		writer.WriteAttributeString('Type', self.DbSvrType.name)
		# -----------------------------------------
		if (self.SQLSvrType != G.SQLSvrType.SQLCE):
			writer.WriteAttributeString('SQLType', self.SQLSvrType.name)

# =====================================================================
# Factory
# =====================================================================
class Factory:

	# -------------------------------------------------
	class Database:
		# ---------------------------------------------
		@staticmethod
		def Create(iD='Database', abbr='Db', sln=None):
			# -----------------------------------------
			if not isinstance(iD, str):
				raise Exception('iD is not string: ' + str(iD))
			if not isinstance(abbr, str):
				raise Exception('abbr is not string: ' + str(abbr))
			# -----------------------------------------
			if (sln == None):
				import Wiz
				sln = Wiz.Solution.Create()
			# -----------------------------------------
			db = Database(sln)
			db.SetID(iD)
			db.Abbr = abbr
			# -----------------------------------------
			assert(len(sln.Databases) == 0)
			sln.AddDatabase(db)
			assert(len(sln.Databases) == 1)
			assert(db == sln.Databases[0])
			assert(db == sln.DatabaseDict[db.ID])
			# -----------------------------------------
			return db

	# -------------------------------------------------
	class Table:
		# ---------------------------------------------
		@staticmethod
		def Create(iD='Table', abbr='Tbl', db=None):
			# -----------------------------------------
			if not isinstance(iD, str):
				raise Exception('iD is not string')
			# -----------------------------------------
			if (db == None):
				db = Factory.Database.Create()
			# -----------------------------------------
			tbl = Table(db)
			tbl.SetID(iD)
			tbl.Abbr = abbr
			tbl.Plural = iD + 's'
			# -----------------------------------------
			db.AddTable(tbl)
			# -----------------------------------------
			return tbl

	# -------------------------------------------------
	class Field:
		# ---------------------------------------------
		@staticmethod
		def Create(iD='Field', tbl=None):
			# -----------------------------------------
			if not isinstance(iD, str):
				raise Exception('iD is not string')
			# -----------------------------------------
			if (tbl == None):
				tbl = Factory.Table.Create()
			# -----------------------------------------
			fld = Field(tbl)
			fld.SetID(iD)
			# -----------------------------------------
			tbl.AddField(fld)
			# -----------------------------------------
			return fld