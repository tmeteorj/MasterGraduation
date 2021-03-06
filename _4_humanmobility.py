
#!/usr/bin/env python
# coding=utf-8
import sys
import time
import random
import os
import gzip
def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
def outputinfo(info,solvecnt,totalcnt,costtime):
    h,m,s=timeEvaluation(solvecnt,totalcnt,costtime)
    print("[%s] %s: completed: %d/%d -> %.3f%%, remain %02d:%02d:%02d\n"%(gettime(),info,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
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
def getmobility(lastmonth,thismonth,removepath,staypath,movepath,newpath):
    global hasha
    fwnw=open(newpath,"w")
    fwst=open(staypath,"w")
    fwmv=open(movepath,"w")
    for line in open(thismonth,"r"):
        info=line.strip().split(",")
        if info[0] in hasha:
            if hasha[info[0]]==info[1]:fwst.write("%s,%s,%s\n"%(info[0],hasha[info[0]],info[1]))
            else:fwmv.write("%s,%s,%s\n"%(info[0],hasha[info[0]],info[1]))
        else:
            fwnw.write(line)
    fwst.close()
    fwmv.close()
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
        getmobility(preffix+month[mo]+".txt",preffix+month[mo+1]+".txt","mobility/remove"+fn,"mobility/stay"+fn,"mobility/move"+fn,"mobility/new"+fn)
        solvecnt+=1
        outputinfo("humanmobility[%s]"%(fn),solvecnt,totalcnt,time.time()-starttime)
