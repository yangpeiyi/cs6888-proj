from process_dot_file import Node 
from process_dot_file import build_tree
from count_branch import count_branch
def dfs(score, fullname_rawname_map, raw_node_map,node,traversed):
    assert isinstance(node, Node)
    traversed.add(node.full_name) #mark the traversed node
    visited = True
    if node.full_name in fullname_rawname_map and node.full_name not in score:
        score[node.full_name]=0 #node is a class, not a function
    for i in node.children:
        if i.full_name not in traversed:
            visited = False
    if visited:#all children are visited/node has no child
        return score[node.full_name]
    total = 0
    for neighbour_node in node.children: #take a neighbouring node
        #whether the neighbour node is already visited
        if neighbour_node.full_name not in traversed: 
            #recursively traverse the neighbouring node
            total+= score[node.full_name]+dfs(score, fullname_rawname_map, raw_node_map,neighbour_node,traversed) 
        else:
            total+= score[neighbour_node.full_name]
    score[node.full_name]=total
    return total


def get_score_map(python_filepath_list,coverage_filepath_list,dot_filepath, uutname):
    traversed=set()
    score = count_branch(python_filepath_list, coverage_filepath_list,uutname=uutname)
    # print(score)
    raw_node_map,fullname_rawname_map = build_tree(dot_filepath=dot_filepath,uutname=uutname)
    # print("raw->node map: ",raw_node_map)
    # print("full->raw map: ",fullname_rawname_map)
    # for name in score:
    #     if name not in fullname_rawname_map:
            # print(name+" not in full->raw map")#ignore

    # print("update score with dfs\n")
    dfs(score, fullname_rawname_map, raw_node_map, raw_node_map["ROOT"], traversed)
    return score
