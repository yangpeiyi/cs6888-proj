###### pydotplus config

python_filepath_list = [
    "/home/ubuntu/.local/lib/python3.8/site-packages/pydotplus/graphviz.py",
    "/home/ubuntu/.local/lib/python3.8/site-packages/pydotplus/parser.py"
]

coverage_filepath_list = [
    "./xmls/graphviz.xml",
    "./xmls/parser.xml"
]

dot_filepath="./pydotplus.dot"
uutname = "pydotplus"
directory = "methods_founded_per_seed" # trace folder
prefix = "./seeds" #seed source
file_extension = "dot"
counts = [10, 20, 30, 40, 50, 60, 70, 80, 90] # value of N

###### end of pydotplus config

import os
from calculate_score import get_score_map 

score = get_score_map(python_filepath_list,coverage_filepath_list,dot_filepath, uutname)
print(score)

res = {}
notfound = set()
for filename in os.listdir(directory):
    file = open(directory+'/' + filename, 'r')
    Lines = file.readlines()
    fullPaths = set()
    for line in Lines:
        if uutname in line:
            lis = line.split(',')
            index = lis[0].find(uutname)
            fileStr = lis[0][index:].strip()
            indexDot = fileStr.find('.')
            fileStr = fileStr[:indexDot]
            fileStr = fileStr.replace('/', "__")

            class_method = lis[-1]
            cmIndex = class_method.find(': ')
            cmStr = class_method[cmIndex + 2:].strip()
            cmStr = cmStr.replace('.', "__")
            fullPath = fileStr + "__" + cmStr
            fullPaths.add(fullPath)


    sum = 0
    for path in fullPaths:
        if path not in score:
            # fullPaths.remove(path)
            notfound.add(path)
        else:
            sum += score[path]

    res[filename] = sum

nres = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
reslist = list(nres.keys())

nprefix = "_top_seeds"

os.system("rm -rf top")
os.system("mkdir top")

print(reslist)
print("nres: ", nres)
for i in range(len(counts)):
    os.system("mkdir top/"+str(counts[i])+nprefix)
    for key in reslist[:int(counts[i] * 0.01 * len(reslist))]:
        key = key.replace("txt", file_extension)
        command = "cp " + prefix + "/" + key + " top/" + str(counts[i]) + nprefix
        # print(command)
        os.system(command)

