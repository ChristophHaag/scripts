#!/usr/bin/env python3

import sys
import glob
import json
import acf
import shutil
import os.path

fromdir = sys.argv[1]
todir = sys.argv[2]

appmanifests = glob.glob(fromdir + "/appmanifest_*.acf")

ids = []
names = []
print("Choose games to move from " + fromdir + " to " + todir)
print("Example: 1-4,5,7-10")
for i, appmanifest in enumerate(appmanifests):
    a = acf.parse_acf(appmanifest)
    appid = appmanifest.split("_")[1].split(".")[0]
    ids.append(appid)
    name = a["AppState"]["name"] if "name" in a["AppState"] else "?????"
    names.append(name)
    print(("{0!s:" + str(len(str(len(appmanifests))) + 1) + "} {1}").format(i, name))

inp = input("> ").split(",")
nums = []
for i in inp:
    if "-" in i:
        start, end = [int(x) for x in i.split("-")]
        for j in range(start,end+1):
            nums.append(j)
    else:
        nums.append(int(i))

print("Moving \"" + "\", \"".join([names[i] for i in nums]) + "\" to " + todir)
confirm = input("Continue (Y/n)? ")
if confirm and confirm.lower() == "n":
    print("Quitting...")
    sys.exit(0)

for num in nums:
    src = appmanifests[num]
    dst = todir + "/" + appmanifests[num].split("/")[-1]
    if not os.path.isfile(dst):
        print("moving " + src + " to " + dst)
        shutil.move(src, dst)    
