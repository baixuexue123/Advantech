
from distutils.core import setup
import py2exe

#要包含的其他库文件
includes = ["encodings", "encodings.*","sip"]
#sip--是pyqt程序需要添加的

options = {"py2exe":
            {"compressed" : 1, #压缩
             "optimize" : 2,
             "ascii" : 1,
             "includes" : includes,
             "bundle_files" : 1
             #1--所有文件打包成一个exe,包括Python解释器
             #2--所有文件打包成一个exe,不包括包括Python解释器
             #3--默认 ,不把所有文件打包成一个exe
            }}

setup(
    name = 'Applaction Name',
    version = '1.0.0.0',
    description = u'---------------',
    author = 'baixue',
    author_email = 'baixuexue123@gmail.com',
    options = options,
    zipfile = None, #不生成library.zip文件
    windows = [{'script' : 'cwac.pyw',
                'icon_resources' : [(1, "images/logo.ico")]}],#源文件和图标
    data_files = ['config.xml',]
    )
