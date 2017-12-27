import re
import os
import glob
import shutil

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
            with open(os.path.join(rootDIR, id + '_'+ month + '.csv'), 'wb') as outfile:
                for i, fname in enumerate(path):
                    with open(fname, 'rb') as infile:
                        if i != 0:
                            infile.readline()  # Throw away header on all but first file
                        shutil.copyfileobj(infile, outfile) # Block copy rest of file from input to output without parsing

