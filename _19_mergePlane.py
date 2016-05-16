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
def find(x):
    global fa
    if x not in fa:
        fa[x]=x
        return x
    else:
        fa[x]=find(fa[x])
        return fa[x]
def merge(x,y):
    global fa
    fx=find(x)
    fy=find(y)
    if fx<fy:fa[fy]=fx
    else:fa[fx]=fy
def mergePlanes(months,planedir):
    fw=open(planedir+"/planeAllNormal.txt","w")
    for mon in months:
        for line in open(planedir+"/planeAllNormal"+mon+".txt","r"):
            info=line.split(",")
            fw.write(mon+"-"+info[0])
            for x in info[1:]:
                fw.write(","+x)
    fw.close()
def loadPlaneInfo(inputpath):
    global fa
    fa=dict()
    for line in open(inputpath,"r"):
        x=line[:line.index(",")]
        fa[x]=x
def getCluster(inputpath,outputpath,T,D):
    global fa
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        ds=float(info[2])
        T-=1
        if ds<=D:merge(info[0],info[1])
        if ds>D or T==0:break
    ans=list()
    for x in fa:
        fx=find(x)
        ans.append([fx,x])
    ans.sort()
    fw=open(outputpath,"w")
    index=0
    last=None
    for xs in ans:
        if last==None or last!=xs[0]:
            index+=1
            last=xs[0]
        fw.write("%s,%d\n"%(xs[1],index))
    fw.close()
if __name__=="__main__":
    global fa
    months=["201412","201501","201502","201503","201504","201505","201506","201507","201508","201509","201510","201511"]
    mergePlane(months,"plane")
    loadPlaneInfo("plane/planeAllNormal.txt")
    print(len(fa))
