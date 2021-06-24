" --------------------------------
" Add our plugin to the path
" --------------------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))

if !exists("g:inkscape_fig_template")
let g:inkscape_fig_template = "
	\ begin{figure}
	\ centering
	\ begin{figure}[ht]
	\ incfig{<+name+>}
	\ chaption{<+title+>}
	\ label{fig:<+name+>}
	\ end{figure}"
endif

" --------------------------------
"  Function(s)
" --------------------------------
function! CreateFig()
python3 << endOfPython
from Inkscape import create

title = vim.current.line
root = vim.eval("b:vimtex.root")
root = root+'/figures'

create(title,root)

endOfPython
endfunction

function! SetupFig()
python3 << endOfPython
from Inkscape import setup
setup()
endOfPython
endfunction


function! EditFig()
python3 << endOfPython
from Inkscape import get_title,edit

title_line = vim.current.line
title = get_title(title_line)
root = vim.eval("b:vimtex.root")
root = root+'/figures'

edit(title,root)

endOfPython
endfunction

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! CreateFig call CreateFig()
command! SetupFig call SetupFig()
command! EditFig call EditFig()

