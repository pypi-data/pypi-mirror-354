#======
#README
#======

#Let's test the source code with our custom checker:

from __future__ import unicode_literals
from __future__ import absolute_import
import p01.checker#>>>
import j01.rater#>>>

checker = p01.checker.Checker()#>>>
checker.check(j01.rater)#>>>
#  -------------
#  img/icons.png
#  -------------
#  0: image bloat found
#        Adobe Photoshop bloat found