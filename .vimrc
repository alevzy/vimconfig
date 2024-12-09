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

" YouCompleteMe settings
packadd YouCompleteMe

let g:ycm_enable_semantic_highlighting=1
