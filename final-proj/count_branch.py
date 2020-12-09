import ast
import tokenize
import intervaltree as intervaltree
import xml.etree.ElementTree as ET
import sys, os

def _compute_interval(node):
    min_lineno = node.lineno
    max_lineno = node.lineno
    for node in ast.walk(node):
        if hasattr(node, "lineno"):
            min_lineno = min(min_lineno, node.lineno)
            max_lineno = max(max_lineno, node.lineno)
    return (min_lineno, max_lineno + 1)

def file_to_tree(filename):
    with tokenize.open(filename) as f:
        parsed = ast.parse(f.read(), filename=filename)
    function_tree = intervaltree.IntervalTree()
    class_tree = intervaltree.IntervalTree()
    for node in ast.walk(parsed):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start, end = _compute_interval(node)
            function_tree[start:end] = node
        elif isinstance(node, (ast.ClassDef)):
            start, end = _compute_interval(node)
            class_tree[start:end] = node
    # print(function_tree,class_tree)
    return function_tree,class_tree

def get_function_name(line_number, python_filepath):
    function_tree,class_tree = file_to_tree(python_filepath)
    
    function_matches = function_tree[line_number]
    assert(function_matches is not None)

    class_matches = class_tree[line_number]
    interval_list = []
    if function_matches:
      for obj in function_matches:
        interval_list.append(obj)
    if class_matches:
      for obj in class_matches:
        interval_list.append(obj)
    interval_list.sort(key=lambda intervalObj:intervalObj[0])#sort based on start
    res = []
    for i in interval_list:
      res.append(i[2].name)
    # print(res)
    function_name = "__".join(res)
    return function_name
    
def count_branch_(python_filepath, coverage_filepath,uutname):
    root = ET.parse(coverage_filepath).getroot()
    function_count={} # function full name:branch count 
    classes = root.findall(".//class")
    lines = []
    assert(len(classes)>0)
    for class_ in classes:
      if "filename" in class_.attrib and class_.attrib["filename"] == python_filepath:
        #   print("processing ",python_filepath)
          lines = class_.getchildren()[1]
    for line in lines:
      if "branch" in line.attrib:
          line_str = ET.tostring(line, 'utf-8', method="xml", short_empty_elements=True)
        #   print(line_str)
          line_number = int(line.attrib["number"])
          branch_count_ = line.attrib["condition-coverage"]
          branch_count = int(branch_count_[branch_count_.index("/")+1])
          function_name = get_function_name(line_number, python_filepath) #only function name
        #   print("function_name:",function_name)
          
          names = python_filepath.split("/")
          name_index = names.index(uutname)
          new_name = "__".join(names[name_index:]).split(".")[0]+"__"

          function_name = new_name+function_name
        #   print("function_name:",function_name)


          if function_name not in function_count:
              function_count[function_name] = 0
          function_count[function_name]+= branch_count
    return function_count

def count_branch(python_filepath_list, coverage_filepath_list,uutname):
  function_count={}
  assert len(python_filepath_list) == len(coverage_filepath_list)
  for (python_filepath, coverage_filepath) in zip(python_filepath_list, coverage_filepath_list):
      # print(python_filepath, coverage_filepath)
      function_count_ = count_branch_(python_filepath, coverage_filepath,uutname)
      # print(function_count_)
      function_count.update(function_count_)
  return function_count