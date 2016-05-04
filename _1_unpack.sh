#!/bin/bash
IFS=,
arrays="201505,201506,201507,201508"
for var in ${arrays[*]}
do
zippath=$var.zip
unzip $zippath
rm -f $zippath
mkdir i$var
done

python _2_infoExtract.py $arrays
python _3_gethome.py $arrays
python _4_humanmobility.py $arrays
