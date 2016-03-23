#!/usr/bin/env python
# coding=utf-8
import sys
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
    for line in open(inputpath,"r"):
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
    month=sys.argv[1:]
    preffix="home/originrealhome"
    loadhash(preffix+month[0]+".txt")
    tot=len(month)
    solvecnt=0
    totalcnt=tot-1
    starttime=time.time()
    for mo in range(tot-1):
        fn=month[mo]+"-"+month[mo+1]+".txt"
        getmobility(preffix+month[mo]+".txt",preffix+month[mo+1],"mobility/remove"+fn,"mobility/stay"+fn,"mobility/new"+fn)
        solvecnt+=1
        h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime())
        print("humanmobility: %s, completed: %d/%d=%.4f%%, remain: %02d:%02d:%02d"%(fn,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
