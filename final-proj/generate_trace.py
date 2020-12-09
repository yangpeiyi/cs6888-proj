## pydotplus config
seed_source = "./seeds"
drivers = ["./drivers/pydotplus_1.py","./drivers/pydotplus_2.py","./drivers/pydotplus_3.py"]
driver_count = len(drivers)
trace_foler= "./methods_founded_per_seed"
file_extension = "dot"
## end of config

import os
import random

#cleanup
os.system("rm "+trace_foler.replace("./","")+" -rf")
os.system("mkdir "+trace_foler.replace("./",""))

for filename in os.listdir(seed_source):
    command = "python3 -m trace --listfuncs "+drivers[random.randint(0,driver_count-1)] +" "+seed_source + "/"+ filename +">"+ trace_foler.replace("./","")+"/"+filename.replace(file_extension,"txt")
    # print(command)
    os.system(command)
