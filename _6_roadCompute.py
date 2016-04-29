#!/usr/bin/env python
# coding=utf-8
#file: length,x1,y1,x2,y2
#59203
import sys
import os
import Queue
import time
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
def outputPoint(inputpath,outputpath):
    p=dict()
    first=True
    index=0
    for line in open(inputpath,"r"):
        if first:
            first=False
            continue
        info=line.strip().split(",")
        for i in range(0,2):
            loc=info[1+i*2]+","+info[2+i*2]
            if loc not in p:
                p[loc]=index
                index=index+1
    fw=open(outputpath,"w")
    for x in sorted(p.items(),key=lambda arg:arg[1]):
        fw.write("%s,%d\n"%(x[0],x[1]))
    fw.close()
def loadPointInfo(inputpath):
    global pmap
    pmap=dict()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        pmap[info[0]+","+info[1]]=int(info[2])
def buildGraph(inputpath):
    global pmap,edge
    edge=dict()
    first=True
    for line in open(inputpath,"r"):
        if first:
            first=False
            continue
        info=line.strip().split(",")
        p1=pmap[info[1]+","+info[2]]
        p2=pmap[info[3]+","+info[4]]
        ds=float(info[0])
        if p1 not in edge:edge[p1]=dict()
        if p2 not in edge:edge[p2]=dict()
        if p1 not in edge[p2]:edge[p2][p1]=ds
        if p2 not in edge[p1]:edge[p1][p2]=ds
def transformGraph(inputpath,outputpath):
    global pmap,edge
    edge=dict()
    first=True
    fw=open(outputpath,"w")
    for line in open(inputpath,"r"):
        if first:
            first=False
            continue
        info=line.strip().split(",")
        p1=pmap[info[1]+","+info[2]]
        p2=pmap[info[3]+","+info[4]]
        ds=float(info[0])
        fw.write("%d %d %f\n"%(p1,p2,ds))
    fw.close()
def spfa(src,fw):
    global edge
    dist=dict()
    pre=dict()
    lis=Queue.deque()
    lis.append(src)
    inQ=dict()
    inQ[src]=True
    pre[src]=-1
    dist[src]=0
    while(len(lis)>0):
        now=lis.popleft()
        inQ[now]=False
        for to in edge[now]:
            ds=edge[now][to]
            if to not in dist or dist[to]>dist[now]+ds:
                pre[to]=now
                dist[to]=dist[now]+ds
                if to not in inQ or inQ[to]==False:
                    inQ[to]=True
                    lis.append(to)
    for id in range(0,59203):
        if id in dist:
            fw.write("%.2f:%d"%(dist[id],pre[id]))
        else:
            fw.write("INF:-1")
        if id==59202:fw.write("\n")
        else:fw.write(",")
if __name__=="__main__":
    #outputPoint("RoadInfo.csv","PointInfo.csv")
    loadPointInfo("PointInfo.csv")
    #buildGraph("RoadInfo.csv")
    transformGraph("RoadInfo.csv","RoadEdge.csv")
    #fw=open("DistanceMat.csv","w")
    #solvecnt=0
    #totalcnt=59203
    #starttime=time.time()
    #for src in range(59203):
    #    spfa(src,fw)
    #    solvecnt=solvecnt+1
    #    outputinfo("SPFA[%d]"%(src),solvecnt,totalcnt,time.time()-starttime)
    #fw.close()
