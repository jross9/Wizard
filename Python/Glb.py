#
# Copyright James Ross (C) 2022
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
import datetime
import time
import tempfile

from enum import Enum, auto

import Dbg

# =====================================================================
# 
# =====================================================================
class Lang(Enum):
	NA = auto()
	Ada = auto()
	Cpp = auto()
	ObjC = auto()
	CSharp = auto()
	Swift = auto()
	Java = auto()
	Scala = auto()
	Perl = auto()
	Php = auto()
	Python = auto()
	Ruby = auto()
	Delphi = auto()
	JavaScript = auto()
	Haxe = auto()
	OCaml = auto()
	
GUI = Enum('GUI', ['NA', 'WinForm', 'WPF', 'WP7', 'SL', 'MonoTouch', 'BB', 'Droid', 'iOS', 'Cocoa', 'MFC', 'VCL', 'WX', 'CGI', 'Php', 'ASP', 'Html5', 'jQM', 'Tk', 'Qt', 'Console', 'WebSVC', 'Daemon', 'Library'])
DataType = Enum('DataType', ['Null', 'Bool', 'Int', 'Enum', 'EnumType', 'String', 'Decimal', 'Float', 'DateTime', 'Image', 'Instance', 'Collection'])
DbType = Enum('DbType', ['Bool', 'Int', 'Enum', 'EnumType', 'String', 'Decimal', 'Float', 'DateTime', 'Image', 'Instance' ,'Collection'])
ScopeType = Enum('ScopeType', ['Private', 'Protected', 'Public'])
TierType = Enum('TierType', ['NA', 'Server', 'Client'])
DeviceType = Enum('DeviceType', ['Mobile', 'PC', 'MAC'])

class VSVers(Enum):
	NA = auto()
	VS5 = auto()
	VS6 = auto()
	VS2003 = auto()
	VS2005 = auto()
	VS2008 = auto()
	VS2010 = auto()
	VS2012 = auto()
	VS2017 = auto()
	VS2019 = auto()
	VS2022 = auto()

class FWVers(Enum):
	NA = auto()
	MTX = auto()
	Net20 = auto()
	Net30 = auto()
	Net35 = auto()
	Net40 = auto()
	Net45 = auto()
	Net472 = auto()
	Net48 = auto()

class FWType(Enum):
	Core = auto()
	Framework = auto()

WinMoVers = Enum('WinMoVers', ['WinCE5', 'WinMo50', 'WinMo60'])
GroupType = Enum('GroupType', ['SingleInstance', 'GroupByType', 'FixedLevel'])
ModelType = Enum('ModelType', ['NA', 'AdoNET', 'SQLiteNET', 'LINQ', 'EF', 'NHibernate'])
DbSvrType = Enum('DbSvrType', ['Access', 'SQLite', 'SQLServer', 'Oracle', 'MySQL', 'PostgreSQL'])
SQLSvrType = Enum('SQLSvrType', ['SQLCE', 'SQLServer', 'SQLExpress', 'LocalDb']) # SQLServer --> Server / Express / LocalDb
WebConfigType = Enum('WebConfigType', ['StandAlone', 'Primary', 'Debug', 'Release'])

# TextAlignType = Enum(['Left', 'Center', 'Right'])
#enum DataStoreType { DB, XML, BIN, TXT }
#enum ClassesGoType { InSeparateFiles, InSingleFile, InMainModule, InLibrary }
#enum ColumnType { Text, Image, ImageText }
#enum ColumnFormatType { Default, ShortDate, LongDate }

# =====================================================================
# 
# =====================================================================
WizDir     = '..'
WizLogPath = WizDir + '/_countLog.txt'
WizPyDir   = WizDir + '/Python'
MkoDefRoot = WizPyDir + '/Templates'
Temp       = tempfile.gettempdir()
MkoTmpFolder = Temp + '/mako_modules'

# =====================================================================
# 
# =====================================================================
CopyAlways = False

# =====================================================================
# 
# =====================================================================
TF_WF    = 0x00000001 # CSharp / WinForm
TF_WPF   = 0x00000002 # CSharp / WPF
TF_WP7   = 0x00000004 # CSharp / WP7
TF_SL    = 0x00000008

TF_MT    = 0x00000010
TF_BB    = 0x00000020
TF_Droid = 0x00000040
TF_iOS   = 0x00000080

TF_Cocoa = 0x00000100
TF_MFC   = 0x00000200
TF_WX    = 0x00000400
TF_CGI   = 0x00000800 # Perl / CGI

TF_Php   = 0x00001000 # Php / CGI
TF_ASP   = 0x00002000 # C#  / ASP.NET (old school)
TF_Html5 = 0x00004000 # JavaScript / HTML5
TF_Tk    = 0x00008000

TF_StdIO = 0x00010000 # a arg can be made that
TF_WS    = 0x00020000 # these kind Console / Service based
TF_SVC   = 0x00040000 # don't need a Per Lang version
TF_Lib   = 0x00080000

TF_PyQt  = 0x00100000
TF_jQM   = 0x00200000
TF_VCL   = 0x00400000

TF_CPP   = 0x100000000000
TF_CS    = 0x200000000000
TF_JAVA  = 0x400000000000
TF_PL    = 0x800000000000
TF_PY    = 0x010000000000

TF_WebOnly = (TF_Html5 | TF_jQM | TF_CGI | TF_ASP)
TF_WinOnly = (TF_WF | TF_WPF | TF_MFC)

# =====================================================================
# SetKey
# =====================================================================
def SetKey(key, value, dict):
	# ---------------------------------------------
	if (key == None):
		raise Exception('KEY can\'t be None')
	# ---------------------------------------------
	if (value == None):
		raise Exception('VALUE can\'t be None')
	# ---------------------------------------------
	if (key not in dict):
		dict[key] = value
	else:
		raise Exception('DUPE KEY [' + key + ']')

# =====================================================================
# pinfo
# =====================================================================
def Print(s, obj=None):
	# ---------------------------------------------
	if (obj != None):
		# -----------------------------------------
		#try:
		#	print('> ' + s + ' => [' + obj.ID + '] ' + str(obj))
		#except:
		#	try:
		#		print('> ' + s + ' => [' + obj.Name + '] ' + str(obj))
		#	except:
		#		print('> ' + s + ' => ' + str(obj))
		# -----------------------------------------
		try:
			print('> ' + s + ' => [' + obj.ID + '] ' + str(obj))
		except:
			print('> ' + s + ' => ' + str(obj))
	# ---------------------------------------------
	else:
		print('> ' + s)

# =====================================================================
# =====================================================================
# VarToLower
# =====================================================================
def VarToLower(var):
	# ---------------------------------------------
	lc_chars = ''
	# ---------------------------------------------
	if (not bool(var)):
		raise Exception('BAD NullOrEmpty VAR NAME')
	elif (var[0].islower()):
		return var # we're already good just return it
	else:
		count = 0
		for ch in var:
			lc_chars += ch.lower()
			if (ch.islower()):
				break
			count += 1
		if (count == len(var)):
			return lc_chars  # all CAPS therefore ALL LOWER Case
		elif (count == 1):
			return lc_chars[:1] + var[1:]
		else:
			return lc_chars[:count-1] + var[count-1:]

# =====================================================================
# 
# =====================================================================
def WriteTmpFile(name, str):
	# ---------------------------------------------
	f = open('C:/Temp/' + name, 'w')
	f.write(str)
	#f.write(bytes(ln + '\n', 'UTF-8'))
	f.close()

# =====================================================================
# 
# =====================================================================
def LogCount(prjCode, logFlg, date_code='1423'):
	# -----------------------------------------------------------------
	f = open(WizLogPath, 'a')
	f.write(date_code + '\t' + prjCode + '\t' + str(datetime.datetime.now()) + '\t' + logFlg + '\n')
	f.close()

# =====================================================================
# 
# =====================================================================
def CreateSlnAndLogIt(sln, logFlg = '-----'):
	# -----------------------------------------------------------------
	t0 = time.perf_counter()
	# -----------------------------------------------------------------
	LogCount(sln.ID, logFlg)
	# -----------------------------------------------------------------
	CreateSolution(sln)
	# -----------------------------------------------------------------
	Dbg.LogIt('elapsed time ' + str(time.perf_counter() - t0))

# =====================================================================
# 
# =====================================================================
def CreateSolution(sln):
	# -----------------------------------------------------------------
	# Dbg.LogIt("# = WriteXmlFile SLN ==> " + sln.ID)
	# sln.WriteXmlFile()
	# -----------------------------------------------------------------
	Dbg.LogIt("# = X2Lang ============> " + sln.ID)
	# -----------------------------------------------------------------
	sln.X2Lang()
	# sln.X2Lang(x2Py=True, x2Haxe=True, x2CS=True)
	# -----------------------------------------------------------------
	# sln.MakeTargets()
	# -----------------------------------------------------------------
	sln.BuildTargets()
	# -----------------------------------------------------------------
	# sln.InitializeObjs()
	# -----------------------------------------------------------------
	Dbg.LogIt("# = WriteXmlFile SLN ==> " + sln.ID)
	sln.WriteXmlFile()
	# -----------------------------------------------------------------
	Dbg.LogIt("# = CREATE ============> " + sln.ID)
	sln.CreateIt()
	# -----------------------------------------------------------------
	Dbg.LogIt("# = SaveIt ============> " + sln.ID)
	sln.SaveIt()
