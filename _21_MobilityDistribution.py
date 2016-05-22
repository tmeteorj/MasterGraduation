import time
import sys
import random
import os
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
    if(sizeF>1):count=int((count+1)*(sizeF+1))
    f.close()
    return count
def loadDistmat(planepath,distpath):
    global dist
    dist=dict()
    pid=[int(t.strip()) for t in open(planepath,"r")]
    for ida,line in zip(pid,open(distpath,"r")):
        ds=[float(t) for t in line.strip().split(",")]
        dist[ida]=dict()
        for idb,x in zip(pid,ds):
            dist[ida][idb]=int(x)
def computeMobPop(mobilitypath,outputpath):
    global dist
    pd=dict()
    for line in open(mobilitypath,"r"):
        info=line.strip().split(",")
        da=int(info[0])
        db=int(info[1])
        ds=dist[da][db]
        np=int(info[2])
        pd[ds]=np if ds not in pd else pd[ds]+np
    fw=open(outputpath,"w")
    for x in sorted(pd.items(),key=lambda arg:arg[0]):
        fw.write("%d,%d\n"%(x[0],x[1]))
    fw.close()
def computeDistPop(mobpoppath,outputpath,maxds,interlen):
    internum=maxds//interlen+1
    pop=[0]*internum
    tot=0
    for line in open(mobpoppath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        idx=info[0]//interlen
        pop[idx]+=info[1]
        tot+=info[1]
    fw=open(outputpath,"w")
    for i in range(iternum+1):
        fw.write("%d,%d,%.6f\n"%(i*interlen+interlen//2,pop[i],float(pop[i])/float(tot)))
    fw.close()
if __name__=="__main__":
    loadDistMat("PlaneInfo.txt","PlaneDist.txt")
    computeMobPop("","")
