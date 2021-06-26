# Inkscape

## Installation

Use your plugin manager of choice.

- [Pathogen](https://github.com/tpope/vim-pathogen)
  - `git clone https://github.com/Lyon52222/Inkscape.vim ~/.vim/bundle/Inkscape.vim`
- [Vundle](https://github.com/gmarik/vundle)
  - Add `Bundle 'https://github.com/Lyon52222/Inkscape.vim'` to .vimrc
  - Run `:BundleInstall`
- [NeoBundle](https://github.com/Shougo/neobundle.vim)
  - Add `NeoBundle 'https://github.com/Lyon52222/Inkscape.vim'` to .vimrc
  - Run `:NeoBundleInstall`
- [vim-plug](https://github.com/junegunn/vim-plug)
  - Add `Plug 'https://github.com/Lyon52222/Inkscape.vim'` to .vimrc
  - Run `:PlugInstall`

## Use
1. Use **:SetupFig** to paste the usepackage and newcommand to current line.
2. Use **:CreateFig** to create a svg with current line as it's name and open it with inkscape.
3. Use **:EditFig** to open svg with inkscape. 

current line should like **\incfig{*name*}**.

4. Use **:CompileFig** to Compile svg to pdf which can import to latex. 

current line should be like **\incfig{ *name* }**

## Todo


1. Add auto compile to pdf
2. Write documentation
