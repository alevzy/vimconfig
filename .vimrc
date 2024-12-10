set nocompatible
filetype plugin on
syntax on
filetype indent on

" show line numbers
set number

set cursorline

" indentation
set tabstop=4
set shiftwidth=4
set expandtab

set incsearch



set t_u7=
set encoding=utf-8

" gruvbox settings
colorscheme gruvbox
set background=dark

" vim-airline settings
let g:airline_theme='base16'

" lsp
packadd lsp
call LspAddServer([#{
            \   name: 'clangd',
            \   filetype: ['c', 'cpp'],
            \   path: '/usr/local/bin/clangd',
            \   args: ['--background-index', '--clang-tidy']
            \   }])
call LspAddServer([#{
            \   name: 'pylsp',
            \   filetype: 'python',
            \   path: '/usr/local/bin/pylsp',
            \   args: []
            \   }])

