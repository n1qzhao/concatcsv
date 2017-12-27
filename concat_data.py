import re
import pandas as pd
import os
import glob

idpattern = re.compile('F....')  # pattern for unit id like F1-01
datepattern = re.compile('20\d{2}\d{2}\d{2}')  # pattern for date like 20170101

rootDIR = os.getcwd()
all_files = []
idset = set()
dateset = set()
monthlist = []

for subdir, dirs, files in os.walk(rootDIR):
    DIR = subdir
    filelist = glob.glob(os.path.join(DIR, "*.csv"))
    all_files.extend(filelist)

for f in all_files:
    id = idpattern.findall(f)
    idset.update(id)  # find all unique unit ids
    date = datepattern.findall(f)
    dateset.update(date)  # find all unique dates

idlist = list(idset)  # transfor into lists so they are iterable
datelist = list(dateset)

for d in datelist:
    monthlist.append(d[0:6])

monthlist = list(set(monthlist))  # find all unique months and turn into list

for id in idlist:
    for month in monthlist:
        path = [p for p in all_files if (id in p) & (month in p)]
        if path:  # if path is not empty
            df = pd.concat((pd.read_csv(fpath, header=0, index_col=None, encoding="gb2312") for fpath in path))
            df.to_csv(os.path.join(rootDIR, id + '_'+ month + '.csv'), header=0, index=False, encoding="gb2312" )
