#!/bin/bash
IFS=,
arrays="201412,201501,201502,201503,201504"
for var in ${arrays[*]}
do
zippath=$var.zip
unzip $zippath
rm -f $zippath
mkdir i$var
echo Finish Unzip $zippath
done

python _2_infoExtract.py
