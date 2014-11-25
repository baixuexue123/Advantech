#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''create a new python module file'''

__author__ = 'baixue'

import os
import sys


fname = '%s.py' % raw_input("FileName:")

#文件是否已经存在
if os.path.exists(fname):
    print "ERROR: '%s' already exists" % fname
    sys.exit()

linelist = [
    '#!/usr/bin/env python',
    '# -*- coding: utf-8 -*-\n',
    '\'\'\'Doc String\'\'\'\n',
    '__author__ = \'baixue\'',
    '\n\n\n\n\n\n\n\n',
    r'if __name__ == "__main__":',
    '    pass'
    ]

# write lines to file
fobj = file(fname, 'w')
fobj.writelines('\n'.join(linelist))
fobj.close()
