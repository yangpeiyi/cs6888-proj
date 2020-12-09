import string

import pydotplus

g = pydotplus.Dot()
g.add_node(pydotplus.Node("test", label=string.printable))
data = g.create(format='jpe')