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
def loadClusterMap(clusterpath):
    global cid
    cid=dict()
    for line in open(clusterpath,"r"):
        info=line.strip().split(",")
        cid[info[0]]=int(info[1])
def computeClusterPopulation(month,inputdir):
    global pop,cid
    pop=dict()
    for line in open(inputdir+"/planeAll"+month+".txt","r"):
        if line.find("PID")==-1:continue
        info=line.strip().split(",")
        key=month+"-"+info[0]
        val=int(info[1])
        idx=cid[key]
        pop[idx]=val if idx not in pop else pop[idx]+val
def outputPopulation(outputpath):
    global pop
    fw=open(outputpath,"w")
    for c in pop:
        fw.write("%d,%d\n"%(c,pop[c]))
    fw.close()
def getAllClusterPopulation(clusterpath,planedir,outputdir):
    loadClusterMap(clusterpath)
    months=["201412"]+[str(t) for t in range(201501,201512)]
    for mon in months:
        computeClusterPopulation(mon,planedir)
        outputPopulation(planedir+"/clusterpop"+mon+".txt")
def loadClusterPopulation(clspoppath):
    global pop
    pop=dict()
    for line in open(clspoppath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        pop[info[0]]=info[1]
def readMobilityMat(mobmatpath):
    global mat
    mat=dict()
    for line in open(mobmatpath,"r"):
        info=line.strip().split(",")
        #a,b,cnt,p
        a=int(info[0])
        b=int(info[1])
        p=float(info[3])
        if a not in mat:mat[a]=dict()
        mat[a][b]=p
def revolution(outputpath,movein):
    global pop,mat,pre
    pre=dict()
    for c in pop:
        if c==-1:continue
        for t in mat[c]:
            p=mat[c][t]
            if t not in pre:pre[t]=0.0
            pre[t]+=pop[c]*mat[c][t]
    if not movein:
        for t in mat[-1]:
            p=mat[-1][t]
            if t not in pre:pre[t]=0.0
            pre[t]+=movein*mat[c][t]
    fw=open(outputpath,"w")
    for c in pre:
        if c==-1:continue
        fw.write("%d,%d\n"%(c,int(pre[c])))
    fw.close()
def revolutionTest(outputdir):
    global pop,mat,pre
    
