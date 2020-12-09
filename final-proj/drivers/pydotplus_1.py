import pydotplus as pydotplus

g = pydotplus.Graph()
s = pydotplus.Subgraph("foo")
g.add_subgraph(s)