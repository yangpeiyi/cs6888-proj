# pydotplus config
import re
import random
import os
seed_source = "./seeds"
drivers = ["./drivers/pydotplus_1.py",
           "./drivers/pydotplus_2.py", 
           "./drivers/pydotplus_3.py"]
driver_count = len(drivers)
seeds_coverages = "./peach_seeds_coverages"
uutname = "pydotplus"
# must be changed to your absolute pydotplus location
package_location = "/home/ubuntu/.local/lib/python3.8/site-packages/pydotplus"
file_extension = "dot"
counts = [10, 20, 30, 40, 50, 60, 70, 80, 90]  # value of N
# end of config

# cleanup
os.system("rm -rf "+seeds_coverages.replace("./", ""))
os.system("mkdir "+seeds_coverages.replace("./", ""))

# generate coverage report(.txt) for each seed
for filename in os.listdir(seed_source):
    command1 = "coverage run " + \
        drivers[random.randint(0, driver_count-1)]+" " + \
        seed_source+"/"+filename+" -L "+package_location
    # print("1:",command1)
    os.system(command1)
    command2 = "coverage report > "+seeds_coverages + \
        "/"+filename.replace(file_extension, "txt")
    # print("2:",command2)
    os.system(command2)


# coverage report(.txt), sort, select top N% and put them into corespoding folders
dictionary = {}
for txt_file in os.listdir(seeds_coverages):
    f = open(seeds_coverages+"/"+txt_file)
    lines = f.readlines()
    stateN = 0
    missN = 0
    for line in lines:
        if uutname in line:
            line = re.sub(" +", " ", line)
            lis = line.split(" ")
            stateN += int(lis[1].strip())
            missN += int(lis[2].strip())
    dictionary[txt_file] = stateN - missN

nres = {k: v for k, v in sorted(
    dictionary.items(), key=lambda item: item[1], reverse=True)}
reslist = list(nres.keys())

print(nres)

nprefix = "_peach_seeds"

os.system("rm -rf peach")
os.system("mkdir peach")

for i in range(len(counts)):
    os.system("mkdir peach/"+str(counts[i])+nprefix)
    for key in reslist[:int(counts[i]*0.01*len(reslist))]:
        key = key.replace("txt", file_extension)
        command = "cp "+seed_source+"/"+key+" peach/"+str(counts[i])+nprefix
        # print(command)
        os.system(command)
