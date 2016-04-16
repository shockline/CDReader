set nocompatible
set backspace=indent,eol,start
filetype on
syntax on

set autoindent
set smartindent
set hls
set nu

set ts=4
set tabstop=4
set expandtab
set shiftwidth=4
set encoding=utf-8

set showmatch
set ruler
set incsearch
set nobackup
set fileencoding=utf-8
set fileencodings=ucs-bom,gb18030,utf-8,default

noremap <c-l> gt<cr>
noremap <c-N> :tabnew <cr>

filetype plugin indent on
autocmd FileType python setlocal et sta sw=4 sts=4

autocmd BufNewFile *.[ch],*.hpp,*.cpp exec ":call SetTitle()" 
autocmd BufNewFile *.py exec ":call SetCommentPy()" 

func SetCommentPy()
    call setline(1,          "#coding=utf8")
    call append(line("."),   "# ========================================================") 
    call append(line(".")+1, "#   Copyright (C) ".strftime("%Y")." All rights reserved.")
    call append(line(".")+2, "#   ") 
    call append(line(".")+3, "#   filename : ".expand("%:t")) 
    call append(line(".")+4, "#   author   : ***")
    call append(line(".")+5, "#   date     : ".strftime("%Y-%m-%d")) 
    call append(line(".")+6, "#   desc     : ") 
    call append(line(".")+7, "# ======================================================== ")
endfunc



func SetComment()
    call setline(1,          "/* ========================================================") 
    call append(line("."),   " *   Copyright (C) ".strftime("%Y")." All rights reserved.")
    call append(line(".")+1, " *   ") 
    call append(line(".")+2, " *   filename : ".expand("%:t")) 
    call append(line(".")+3, " *   author   : ***")
    call append(line(".")+4, " *   date     : ".strftime("%Y-%m-%d")) 
    call append(line(".")+5, " *   info     : ") 
    call append(line(".")+6, " * ======================================================== */")
    call append(line(".")+7, "")
endfunc

func SetTitle()
    call SetComment()
    if expand("%:e") == 'hpp' 
        call append(line(".")+8, "#ifndef _".toupper(expand("%:t:r"))."_H") 
        call append(line(".")+9, "#define _".toupper(expand("%:t:r"))."_H") 
        call append(line(".")+10, "#ifdef __cplusplus") 
        call append(line(".")+11, "extern \"C\"") 
        call append(line(".")+12, "{") 
        call append(line(".")+13, "#endif") 
        call append(line(".")+14, "") 
        call append(line(".")+15, "#ifdef __cplusplus") 
        call append(line(".")+16, "}") 
        call append(line(".")+17, "#endif") 
        call append(line(".")+18, "#endif //".toupper(expand("%:t:r"))."_H") 
    elseif expand("%:e") == 'h' 
        call append(line(".")+8, "#ifndef _".toupper(expand("%:t:r"))."_H") 
        call append(line(".")+9, "#define _".toupper(expand("%:t:r"))."_H") 
        call append(line(".")+10, "")
        call append(line(".")+11, "")
        call append(line(".")+12, "")
        call append(line(".")+13, "")
        call append(line(".")+14, "#endif //".toupper(expand("%:t:r"))."_H") 
    elseif expand("%:e") == 'c'
        call append(line(".")+8,"#include \"".expand("%:t:r").".h\"") 
    elseif &filetype == 'cpp' 
        call append(line(".")+8, "#include \"".expand("%:t:r").".h\"") 
    endif
endfunc

