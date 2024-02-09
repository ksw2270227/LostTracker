import os

def list_files(startpath, file_name):
    with open(file_name, 'w',encoding='utf-8') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for file in files:
                f.write('{}{}\n'.format(subindent, file))

# ここにFlaskプロジェクトのルートディレクトリを指定してください
startpath = './'

# 出力されるテキストファイルの名前
file_name = 'directory_structure.txt'

list_files(startpath, file_name)
