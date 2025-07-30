#======
#README
#======

#Let's test the source code with our custom checker:

from __future__ import absolute_import
import p01.checker#>>>
import j01.dialog#>>>
skipFolderNames = [#>>>
    'test'#...
]#...

checker = p01.checker.Checker()#>>>
checker.check(j01.dialog, skipFolderNames=skipFolderNames)#>>>
