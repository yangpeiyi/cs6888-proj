import pydotplus

graph_data = 'graph A { a->b };\ngraph B {c->d}'
graphs = pydotplus.graph_from_dot_data(graph_data)