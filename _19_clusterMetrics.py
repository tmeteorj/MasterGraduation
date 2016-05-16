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
def loadDist(inputpath):
    global dist,pid
    dist=dict()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        p=info[:2]
        if p[0]>p[1]:p=[p[1],p[0]]
        dist[p[0]][p[1]]=float(info[2])
def loadPlane(inputpath):
    global pid
    pid=dict()
    index=0
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        pid[info[0]]=[float(t) for t in info[1:]]
        index+=1
def sortCluster(inputdir,outputdir):
    files=os.listdir(inputdir)
    for f in files:
        l=list()
        for line in open(inputdir+"/"+f,"r"):
            info=line.strip().split(",")
            l.append([int(info[1]),info[0]])
        l.sort()
        fw=open(outputdir+"/"+f,"w")
        for x in l:
            fw.write("%s,%d\n"%(x[1],x[0]))
        fw.close()
def distance(a,b):
    ans=0.0
    for x,y in zip(a,b):
        ans+=(float(x)-float(y))**2
    return ans
def computeMetrics(K,clusterpath,size):
    global pid,dist
    cen=[None]*K
    avg=[None]*K
    last=None
    ls=list()
    for line in open(clusterpath):
        info=line.strip().split(",")
        info[1]=int(info[1])
        if last==None:
            last=info[1]
        if last!=info[1]:
            res=0
            tot=len(ls)
            cen[last]=[0]*size
            for x in ls:
                data=pid[x]
                for y,yid in zip(data,range(size)):
                    cen[last][yid]+=y
            cen[last]=[float(t)/tot fot t in cen[last]]
            for x in ls:
                for y in ls:
                    if x>=y:continue
                    res+=dist[x][y]
            res=2.0*res/(tot*(tot-1.0))
            avg[last]=res
            last=info[1]
            ls.clear()
        ls.append(info[0])
    res=0
    tot=len(ls)
    cen[last]=[0]*size
    for x in ls:
        data=pid[x]
        for y,yid in zip(data,range(size)):
            cen[last][yid]+=y
    cen[last]=[float(t)/tot fot t in cen[last]]
    for x in ls:
        for y in ls:
            if x>=y:continue
            res+=dist[x][y]
    res=2.0*res/(tot*(tot-1.0))
    avg[last]=res
    dbi=0.0
    for i in avg:
        mx=0.0
        for j in avg:
            if i==j:continue
            mx=max(mx,(avg[i]+avg[j])/distance(cen[i],cen[j]))
        dbi+=mx
    dbi/=float(K)
    return dbi
def KMeansMetrics(KS,clusterdir,size,outputpath):
    fw=open(outputpath,"w")
    for k in KS:
        dbi=computeMetrics(k,clusterdir+"/clus_euc_%s.txt"%(k),size)
        fw.write("%s,%.5f\n"%(k,dbi))
    fw.close()
if __name__=="__main__":
    KMeansMetrics(sys.argv[1:],"cluster",19,"cluster")
