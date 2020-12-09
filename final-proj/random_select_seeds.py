## pydotplus config
file_extension = "dot"
seed_source = "./seeds"
percentages = [10,20,30,40,50,60,70,80,90]
## end of pydotplus config
import sys,os,random
nprefix = "_random_seeds"

os.system("rm -rf random")
os.system("mkdir random")

total = len(os.listdir(seed_source)) #number of file in source
for percentage in percentages:
    os.system("mkdir random/"+str(percentage)+nprefix)
    s=set()
    while len(s) < int(percentage*0.01*total):
        s.add(random.randint(0,total-1))
    for i in s:
        filename = os.listdir(seed_source)[i]
        command = "cp " + seed_source+"/"+filename +" " + "random/"+str(percentage)+nprefix
        # print(command)
        os.system(command)