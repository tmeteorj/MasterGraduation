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
    if(sizeF>1):count=int(count*sizeF)
    f.close()
    return count
def isNum(val):
    return re.compile(r"^\d+(.\d+)?$").match(val)!=None
def distance(a,b):
    global distmethod
    if distmethod=="euc":
        ds=0.0
        for p in zip(a,b):
            if isNum(p[0]):
                p=[float(t) for t in p]
                ds+=(p[0]-p[1])**2
            elif p[0]!=p[1]:
                ds+=1.0
        return ds
    elif distmethod=="cos":
        top=0.0
        bota=0.0
        botb=0.0
        for p in zip(a,b):
            if isNum(p[0]):
                p=[float(t) for t in p]
                top+=p[0]*p[1]
                bota+=p[0]*p[0]
                botb+=p[1]*p[1]
            else:
                if p[0]==p[1]:top+=1.0
                bota+=1.0
                botb+=1.0
        bot=math.sqrt(bota)*math.sqrt(botb)
        return top/bot
    elif distmethod=="man":
        ds=0.0
        for p in zip(a,b):
            if isNum(p[0]):
                p=[float(t) for t in p]
                ds+=math.abs(p[0]-p[1])
            elif p[0]!=p[1]:
                ds+=1.0
        return ds
def merge(a,b):
    global clumethod,dist,cluster
    if clumethod=="longest":
        for c in cluster:
            if c!=a and c!=b:
                dist[a][c]=max(dist[a][c],dist[b][c])
                dist[c][a]=dist[a][c]
    elif clumethod=="nearest":
        for c in cluster:
            if c!=a and c!=b:
                dist[a][c]=min(dist[a][c],dist[b][c])
                dist[c][a]=dist[a][c]
    for x in cluster[b]:
        cluster[a][x]=cluster[b][x]
    cluster.pop(b)
    dist.pop(b)
def loadClusterFile(preffix,inputpath):
    global cluster
    fisrt=True
    for line in open(inputpath,"r"):
        if first:
            first=False
            continue
        info=line.strip().split(",")
        name=preffix+"-"+info[0]
        cluster[key]=dict()
        cluster[key][key]=info[1:]
def loadClusterAll(months,planedir):
    global cluster,dist
    cluster=dict()
    dist=dict()
    for month in months:
        loadClusterFile(month,planedir+"/planeAllNormal"+month+".txt")
    for a in cluster:
        for b in cluster:
            if a==b:ds=0
            else:ds=distance(cluster[a][a],cluster[b][b])
            if a not in dist:dist[a]=dict()
            if b not in dist:dist[b]=dict()
            dist[a][b]=ds
            dist[b][a]=ds
def iteration(minds):
    global cluster,dist
    mina=-1
    minb=-1
    for a in cluster:
        for b in cluster:
            if b<=a:continue
            ds=dist[a][b]
            if ds<minds:
                minds=ds
                mina=a
                minb=b
    if mina==-1:return False
    merge(mina,minb)
    return True
def planeCluster(K,D,outputpath):
    global cluster
    tot=len(cluster)
    totalcnt=tot-K
    startime=time.time()
    for i in range(totalcnt):
        flag=iteration(D)
        outputinfo("planeCluster[%d,%.4f]"%(K,D),i+1,totalcnt,time.time()-starttime)
        if not flag:break
    index=0
    fw=open(outputpath,"w")
    for c in cluster:
        index+=1
        for x in cluster[c]:
            fw.write("%d,%s"%(index,x))
            for a in cluster[c][x]:fw.write(","+a)
            fw.write("\n")
    fw.close()
if __name__=="__main__":
    global clumethod,distmethod
    clumethod=sys.argv[1]
    distmethod=sys.argv[2]
    K=int(sys.argv[3])
    D=float(sys.argv[4])
    months=sys.argv[5:]
    loadClusterAll(months,"plane")
    planeCluster(K,D,"cluster/clu_%d_%.4f.txt"%(K,D))
