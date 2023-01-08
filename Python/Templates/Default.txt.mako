<% Txt = file.MakoSource(context) %>\
Default Mako Template

Must Override!

From solution: ${sln.ID}!!
## ----------------------------------------------
% if file is UNDEFINED:
File: UNDEFINED
% else:
From File / Module: ${file.FilePath} 
% endif
## ----------------------------------------------
% if tgt is UNDEFINED:
Target: UNDEFINED
% else:
Target: ${tgt.ID}
% endif
##
##
-------------------------------------------
<%
    Txt.TabInc()
    for x in range(19):
        Txt.Code('Line ' + str(x+1) + '!')
    Txt.TabDec()
%>\
-------------------------------------------
<% file.TestContext2(context) %>\
${file.TestContext(context)}
