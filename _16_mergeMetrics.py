import time
import sys
import random
import os
import psutil
import math
def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
def outputinfow(info):
    print("[%s] %s\n"%(gettime(),info))
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
def loadPlaneMetricsFile(inputpath,startid,head,plane):
    outputinfow("start loadPlaneMetrics[%s]"%(inputpath))
    for line in open(inputpath,"r"):
        if head:
            head=False
            continue
        info=line.strip().split(",")
        pid=info[0]
        if pid not in plane:
            #plane[pid]=[
            #0   population,calloutcnt,callincnt,callouttime,callintime,calltime,messoutcnt,messincnt,messouttime,messintime,messtime,
            #11  calldegree,messdegree
            #13  callcomcnt,messcomcnt
            #15  callmessnmi,callentropy,messentropy]
            plane[pid]=[0,0,0,0,0, 0,0,0,0,0, 0,0,0,0,0, 0,0,0]
        for x in info[1:]:
            plane[pid][startid]=x
            startid=startid+1
    outputinfow("end loadPlaneMetrics[%s]"%(inputpath))
def loadPlaneMetricsMonth(planedir,month):
    plane=dict()
    loadPlaneMetricsFile(planedir+"/communicationInter"+month+".txt",0,True,plane)
    loadPlaneMetricsFile(planedir+"/degree"+month+".txt",11,False,plane)
    loadPlaneMetricsFile(planedir+"/comcnt"+month+".txt",13,False,plane)
    loadPlaneMetricsFile(planedir+"/communityMetrics"+month+".txt",15,False,plane)
    fw=open(planedir+"/planeAll"+month+".txt","w")
    for x in sorted(plane.items(),key=lambda arg:int(arg[0])):
        fw.write(x[0])
        for i in x[1]:
            fw.write(","+i)
        fw.write("\n")
    fw.close()
if __name__=="__main__":
    months=sys.argv[1:]
    solvecnt=0
    totalcnt=len(months)
    starttime=time.time()
    for month in months:
        loadPlaneMetricsMonth("plane",month)
        solvecnt+=1
        outputinfo("loadPlaneMetrics[%s]"%(month),solvecnt,totalcnt,time.time()-starttime)
