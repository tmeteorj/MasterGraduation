import time
import sys
import random
import os
import math
import re
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
def loadClusterMap(inputpath):
    global cid
    cid=dict()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        cid[info[0]]=int(info[1])
def readMobilityFile(inputpath):
    global cid,cmat
    ms=inputpath[inputpath.index["2"]:inputpath.index["."]].split("-")
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        pid=[None,None]
        for i in range(2):
            if info[i]=="-1":
                pid[i]=-1
                continue
            pid[i]=cid[ms[i]+"-"+info[i]]
        if pid[0] not in cmat:cmat[pid[0]]=dict()
        if pid[1] not in cmat[pid[0]]:cmat[pid[0]][pid[1]]=0
        cmat[pid[0]][pid[1]]+=int(info[2])
        cmat[pid[0]][-2]+=int(info[2])
def readMobilityDir(inputdir,single):
    global cmat
    cmat=dict()
    files=os.listdir(inputdir)
    solvecnt=0
    totalcnt=len(files)
    starttime=time.time()
    for f in files:
        if f.find("mat")==0:
            readMobilityFile(inputdir+"/"+f)
            if single:
                outputClusterMobility(inputdir+"/clustermobility"+f[f.index("2"):])
                cmat=dict()
        solvecnt+=1
        outputinfo("readMobilityDir(%s)"%(f),solvecnt,totalcnt,time.time()-starttime)
    if not single:
        outputClusterMobility(inputdir+"/clustermobilityAll.txt")
def outputClusterMobility(outputpath):
    global cmat
    fw=open(outputpath,"w")
    for x in sorted(cmat.items,key=lambda arg:arg[0]):
        data=x[1]
        tot=0
        for y in sorted(data.items(),key=lambda arg:arg[0]):
            if y[0]==-2:
                tot=y[1]
                continue
            fw.write("%d,%d,%d,%.4f\n"%(x[0],y[0],y[1],float(y[1])/float(tot)))
    fw.close()
if __name__=="__main__":
    global cmat
    loadClusterMap("cluster/clus_euc_270.txt")
    readMobilityDir("mobilitymat",False)
    readMobilityDir("mobilitymat",True)

