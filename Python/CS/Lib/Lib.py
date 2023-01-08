#
# Copyright James Ross (C) 2023
#
# Released under the GNU AFFERO GENERAL PUBLIC LICENSE Version 3
# Please see README.md, LICENSE, agpl-3.0.txt in root folder
#
from __future__ import annotations

import Glb as G
# import Base
import Wiz
import CS

# =====================================================================
# Target
# =====================================================================
class Target(CS.Target):

	def __init__(self, parent):
		super().__init__(parent)

	# ---------------------------------------------
	# STATIC METHODS
	# ---------------------------------------------
	@staticmethod
	def MAKE(iD:str, parent:Wiz.Folder) -> Target:
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
	def XmlName(self):
		# -----------------------------------------
		return 'CSharp.Lib'