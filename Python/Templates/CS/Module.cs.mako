using System;
using System.Collections.Generic;
using System.Text;

namespace ${mod.Namespace}
{
	// Solution -> ${sln.ID}
	// Module -> ${mod.FilePath}
	% if tgt is UNDEFINED:
	// Target -> UNDEFINED
	% else:
	// Target -> ${tgt.ID}
	% endif
}