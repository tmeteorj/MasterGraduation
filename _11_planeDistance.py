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
def sortBasePointMap(basepointpath,keypointpath):
    res=dict()
    for line in open(basepointpath,"r"):
        info=line.strip().split(",")
        res[info[0]]=int(info[1])
    fw1=open(basepointpath,"w")
    fw2=open(keypointpath,"w")
    lastk=-1
    for x in sorted(res.items(),key=lambda arg:arg[1]):
        fw1.write("%s,%d\n"%(x[0],x[1]))
        if lastk!=-1 and lastk!=x[1]:
            fw2.write("%d\n"%(lastk))
        lastk=x[1]
    if lastk!=-1:fw2.write("%d\n"%(lastk))
    fw1.close()
    fw2.close()
def keepKeyPoint(keypointpath,matdir,outputpath):
    s=set()
    for line in open(keypointpath,"r"):
        s.add(int(line.strip()))
    s=list(s)
    s.sort()
    fw=open(outputpath,"w")
    op=-1
    nl=-1
    solvecnt=0
    totalcnt=len(s)
    starttime=time.time()
    for linenum in s:
        tof=linenum/1000
        tol=linenum%1000
        if op==-1 or op!=tof:
            nl=0
            op=linenum/1000
            fr=open(matdir+"/MatDist"+str(op)+".txt","r")
        while nl<=tol:
            line=fr.readline()
            nl=nl+1
        info=line.strip().split(" ")
        first=True
        for x in s:
            if first:first=False
            else:
                fw.write(",")
            fw.write(info[x])
        fw.write("\n")
        solvecnt=solvecnt+1
        outputinfo("KeepKeyPoint[%d]"%(linenum),solvecnt,totalcnt,time.time()-starttime)
    fw.close()
def loadKeyDist(keypath,distpath):
    global dist
    dist=dict()
    l=list()
    for line in open(keypath,"r"):
        t=int(line.strip())
        l.append(t)
        dist[t]=dict()
    tot=len(l)
    i=0
    for line in open(distpath,"r"):
        d=[float(t) for t in line.strip().split(",")]
        for j in range(i+1,tot):
            dist[l[i]][l[j]]=d[j]
        i=i+1
def loadBaseMap(basepointpath):
    global basep
    basep=dict()
    for line in open(basepointpath):
        info=line.strip().split(",")
        basep[info[0]]=int(info[1])
def computeDist(pa,pb):
    global dist
    ans=0.0
    for a in pa:
        for b in pb:
            if a<b:ans=ans+dist[a][b]
            elif b<a:ans=ans+dist[b][a]
    tot=len(pa)*len(pb)
    return ans/tot
def getPlaneDist(baseplanemappath,planedistpath):
    global basep
    plane=dict()
    for line in open(baseplanemappath,"r"):
        info=line.strip().split(",")
        if info[3] not in plane:plane[info[3]]=list()
        plane[info[3]].append(basep[info[0]])
    fw=open(planedistpath,"w")
    plane=sorted(plane.items(),key=lambda arg:int(arg[0]))
    solvecnt=0
    totalcnt=len(plane)
    starttime=time.time()
    for a in plane:
        first=True
        for b in plane:
            if first:first=False
            else:fw.write(",")
            if(a[0]==b[0]):fw.write("0")
            else:fw.write(str(computeDist(a[1],b[1])))
        fw.write("\n")
        solvecnt=solvecnt+1
        outputinfo("getPlane[%s]"%(a[0]),solvecnt,totalcnt,time.time()-starttime)
    fw.close()
if __name__=="__main__":
    sortBasePointMap("data/BasePointMap.txt","data/KeyPoint.txt")
    keepKeyPoint("data/KeyPoint.txt","Mat","data/KeyDist.txt")
    loadBaseMap("data/BasePointMap.txt")
    loadKeyDist("data/KeyPoint.txt","data/KeyDist.txt")
    getPlaneDist("data/BasePlaneSimple.csv","data/PlaneDist.txt")
