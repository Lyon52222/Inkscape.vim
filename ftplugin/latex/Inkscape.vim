" --------------------------------
" Add our plugin to the path
" --------------------------------
python3 import sys
python3 import vim
python3 sys.path.append(vim.eval('expand("<sfile>:h")'))

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

" --------------------------------
"  Expose our commands to the user
" --------------------------------
command! CreateFig call CreateFig()
