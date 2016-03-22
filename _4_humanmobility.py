#!/usr/bin/env python
# coding=utf-8
import time
import random
import os
import gzip
def timeEvaluation(solvecnt,totalcnt,costtime):
    if solvecnt>=totalcnt:
        return 0,0,0
    avetime=costtime*1.0/solvecnt
    remaintime=avetime*(totalcnt-solvecnt)
    hour=remaintime//3600
    minu=remaintime%3600/60
    secs=int(remaintime%60)
    return hour,minu,secs
def countline(filePath):
    f=open(filePath,"rb")
    sizeF=os.path.getsize(filePath)/1024/1024/1024
    buff=f.read(1024*1024*1024)
    count=buff.count("\n")
    if(sizeF>1):count=int(count*sizeF)
    f.close()
    return count
def loadhash(inputpath):
    global hasha
    hasha=dict()
    for line in open(lastmonth,"r"):
        info=line.strip().split(",")
        hasha[info[0]]=info[1]
def getmobility(lastmonth,thismonth,removepath,staypath,newpath):
    global hasha
    fwnw=open(newpath,"w")
    fwst=open(staypath,"w")
    for line in open(thismonth,"r"):
        info=line.strip().split(",")
        if info[0] in hasha:
            fwst.write("%s,%s,%s\n"%(info[0],hasha[info[0]],info[1]))
        else:
            fwnw.write(line)
    fwst.close()
    fwnw.close()
    loadhash(thismonth)
    fwrm=open(removepath,"w")
    for line in open(lastmonth,"r"):
        info=line.strip().split(",")
        if info[0] not in hasha:
            fwrm.write(line)
    fwrm.close()
if __name__=="__main__":
    preffix="home/originrealhome"
    loadhash(preffix+"201412.txt") 
    month=["201412","201501","201502","201503","201504","201505","201506","201507","201508"]
    for mo in range(8):
        fn=month[mo]+"-"+month[mo+1]+".txt"
        getmobility(preffix+month[mo]+".txt",preffix+month[mo+1],"mobility/remove"+fn,"mobility/stay"+fn,"mobility/new"+fn)