import argparse
import os
import subprocess
import shutil

VIM_PACK_DIR = os.path.expanduser('~/.vim/pack')

class Plugin:
    def __init__(self, name, url, vimdir):
        self.__name = name
        self.__url = url
        self.__vimdir = vimdir
        self.__shell_commands = list()
        self.__git_options = [] 
    
    @property
    def name(self):
        return self.__name
    @property
    def url(self):
        return self.__url
    @property
    def vimdir(self):
        return self.__vimdir
    @property
    def git_options(self):
        return self.__git_options
    @git_options.setter
    def git_options(self, value):
        self.__git_options = value
    def add_shell_command(self, command, cwd=None):
        self.__shell_commands.append({'command': command, 'cwd': cwd})
    def add_helptags(self, helptags):
        self.add_shell_command(f'vim -u NONE -c "helptags {helptags}" -c q')
    def iterate_commands(self):
        for command in self.__shell_commands:
            yield command

plugins = dict()
plugins['fugitive'] = Plugin('fugitive', 'https://github.com/tpope/vim-fugitive.git', 'tpope/start/fugitive')
plugins['fugitive'].add_helptags('fugitive/doc')
plugins['NERDTree'] = Plugin('NERDTree', 'https://github.com/preservim/nerdtree.git', 'vendor/start/nerdtree')
plugins['NERDTree'].add_helptags(os.path.join(VIM_PACK_DIR, 'vendor/start/nerdtree/doc'))
plugins['vim-airline'] = Plugin('vim-airline', 'https://github.com/vim-airline/vim-airline', 'dist/start/vim-airline')
plugins['vim-airline'].add_helptags(os.path.join(VIM_PACK_DIR, 'dist/start/vim-airline/doc'))
plugins['vim-airline-themes'] = Plugin('vim-airline-themes', 'https://github.com/vim-airline/vim-airline-themes', 'dist/start/vim-airline-themes')
plugins['vim-airline-themes'].add_helptags(os.path.join(VIM_PACK_DIR, 'dist/start/vim-airline-themes/doc'))
plugins['gruvbox'] = Plugin('gruvbox', 'https://github.com/morhetz/gruvbox.git', 'default/start/gruvbox')
plugins['LSP'] = Plugin('LSP', 'https://github.com/yegappan/lsp.git', 'downloads/opt/lsp')
plugins['LSP'].add_helptags(os.path.join(VIM_PACK_DIR, 'downloads/opt/lsp/doc'))

def download(clone_dir):
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    # possibly clean the directory
    for plugin in plugins.values():
        print(f'Downloading {plugin.name}...')
        path = os.path.join(clone_dir, plugin.name)
        if os.path.exists(path):
            shutil.rmtree(path)
        subprocess.run(['git', 'clone'] + plugin.git_options + [plugin.url, path])
        print('Done')

def install(clone_dir):
    for plugin in plugins.values():
        print(f'Installing {plugin.name}')
        install_path = os.path.join(VIM_PACK_DIR, plugin.vimdir)
        if os.path.exists(install_path):
            shutil.rmtree(install_path)
        if clone_dir is None:
            source_path = plugin.url
            subprocess.run(['git', 'clone'] + plugin.git_options + [source_path, install_path])
        else:
            source_path = os.path.join(clone_dir, plugin.name)
            print(f'Copy from {source_path} to {install_path}...')
            shutil.copytree(source_path, install_path, dirs_exist_ok=True)
            print(f'OK')
        for command in plugin.iterate_commands():
            subprocess.run(command['command'], shell=True, cwd=command['cwd'])
        print(f'Done')    
    shutil.copyfile(os.path.abspath('./.vimrc'), os.path.expanduser('~/.vimrc'))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--clonedir', type=str)
    parser.add_argument('--download', action='store_true')
    parser.add_argument('--install', action='store_true')
    args = parser.parse_args()
    clone_dir = args.clonedir
    download_flag = args.download
    install_flag = args.install
    
    if clone_dir is not None and download_flag:
        download(clone_dir)
    if install_flag:
        install(clone_dir)

if __name__ == '__main__':
    main()
