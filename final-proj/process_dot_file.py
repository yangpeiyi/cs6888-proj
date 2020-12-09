import pydot
import pyparsing
import json

class Node():
  def __init__(self, raw_name, full_name, ):
    self.full_name = full_name
    self.raw_name = raw_name
    self.children = []
    self.parents = []
    self.score = 0

  def get_children(self):
    return self.children
  
  def add_child(self,node):
    self.children.append(node)
  
  def get_parents(self):
    return self.parents
  
  def add_parent(self,node):
    self.parents.append(node)

  def __str__(self):
    return "fullname: "+self.full_name+", raw name: "+self.raw_name

def build_tree(dot_filepath,uutname):
  graph = pydot.graph_from_dot_file(dot_filepath)
  raw_node_map = {}
  fullname_rawname_map = {}
  all_subgraphs = graph[0].get_subgraph("cluster_G")[0].obj_dict['subgraphs']
  for unique_subgraph_name in all_subgraphs:
    subgraphs = all_subgraphs[unique_subgraph_name]
    for subgraph in subgraphs:
      nodes = subgraph["nodes"]
      for node_key in nodes:
        if node_key!="graph":
          # print("node_key:  ",node_key)#raw
          label = nodes[node_key][0]["attributes"]["label"]
          # print("label:  ",label)#raw
          labels = label.split("/")
          
          label_index = labels.index(uutname)
          key_index = 0
          new_label = "__".join(labels[label_index:]).split(".")[0]
          # print("new_label:",new_label)
          new_string = ""
          pointer=0
          while pointer<len(new_label) and pointer<len(node_key):
            if new_label[pointer] == node_key[pointer]:
              new_string+=new_label[pointer]
              pointer+=1
            else:
              break
          new_string+=new_label[pointer:]
          if pointer!=len(new_label):
            new_string+="__"
          new_string+=node_key[pointer:]
          # print("new_string:",new_string)
          # print("\n\n")
          node = Node(node_key, new_string)#raw, fullname
          raw_node_map[node_key] = node
          fullname_rawname_map[new_string] = node_key

  edgeList = graph[0].get_edge_list() 
  for e in edgeList:
    src = e.get_source()#raw
    des = e.get_destination()
    # print(src,des)

    if src not in raw_node_map:
      raw_node_map[src] = Node(src, src.replace(".","__"))
      fullname_rawname_map[src] = src.replace(".","__")
    
    if des not in raw_node_map:
      raw_node_map[des] = Node(des, des.replace(".","__"))
      fullname_rawname_map[des] = des.replace(".","__")

    src_node = raw_node_map[src]
    des_node = raw_node_map[des]
    
    src_node.add_child(des_node)
    des_node.add_parent(src_node)

  assert len(raw_node_map) == len(fullname_rawname_map)

  root = Node("ROOT","ROOT")
  raw_node_map["ROOT"] = root
  fullname_rawname_map["ROOT"]="ROOT"

  for raw_name in raw_node_map:
    node = raw_node_map[raw_name]
    if len(node.parents) == 0:
      root.add_child(node)
      node.add_parent(root)

  # testing
  # for key in raw_node_map:
  #   print(key, raw_node_map[key])

  return raw_node_map,fullname_rawname_map