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
def isNum(val):
    return True
  #  return re.compile(r"^\d+(.\d+)?$").match(val)!=None
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
    global clumethod,dist,removed
    if clumethod=="longest":
        for c in dist:
            if c!=a and c!=b:
                if c<a:
                    if dist[c][a]<dist[c][b]:
                        dist[c][a]=dist[c][b]
                        removed.add()
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
def computeDistAll(planedir,months,outputdir):
    global distmethod
    sam=dict()
    for month in months:
        for line in open(planedir+"/planeAllNormal"+month+".txt","r"):
            info=line.strip().split(",")
            sam[month+"-"+info[0]]=info[1:]
    solvecnt=0
    totalcnt=len(sam)*3
    starttime=time.time()
    for meth in ["euc","cos","man"]:
        distmethod=meth
        fw=open(outputdir+"/dist_"+meth+".txt","w")
        for a in sam:
            for b in sam:
                if a>b:continue
                fw.write("%s,%s,%f\n"%(a,b,distance(sam[a],sam[b])))
            solvecnt+=1
            if random.random()*100<1:
                outputinfo("computeDistAll[%s]"%(meth),solvecnt,totalcnt,time.time()-starttime)
        fw.close()
def loadDistFile(inputpath):
    global dist,pmap
    init_heap()
    dist=dict()
    solvecnt=0
    totalcnt=countline(inputpath)
    rate=totalcnt/10000
    starttime=time.time()
    lasttime=time.time()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        ua=pmap[info[0]]
        ub=pmap[info[1]]
        if ua>ub:ua,ub=swap(ua,ub)
        if ua not in dist:dist[ua]=dict()
        dist[ua][ub]=float(info[2])
        push([float(info[2]),ua,ub])
        solvecnt+=1
        if time.time()-lasttime>=10:
            lasttime=time.time()
            outputinfo("loadDistFile(%s)"%(inputpath),solvecnt,totalcnt,lasttime-starttime)
def iteration(logs):
    global dist
    minds=1000.0
    mina=-1
    minb=-1
    for a in dist:
        for b in dist:
            if b<=a:continue
            ds=dist[a][b]
            if ds<minds:
                minds=ds
                mina=a
                minb=b
    if mina!=-1:
        merge(mina,minb)
        logs.write("%s,%s,%f\n"%(mina,minb,minds))
    else:
        print("merge error")
        logs.close()
        sys.exit(-1)
    return minds
def planeCluster(mergepath):
    global dist
    logs=open(mergepath,"w")
    tot=len(dist)
    totalcnt=tot-1
    startime=time.time()
    for i in range(totalcnt):
        minds=iteration(logs)
        outputinfo("planeCluster[%s,%.4f]"%(mergepath,minds),i+1,totalcnt,time.time()-starttime)
    logs.close()
def sortDist(inputdir,outputpath):
    ds=list()
    solvecnt=0
    totalcnt=countline("cluster/dist_cos.txt")+countline("cluster/dist_euc.txt")+countline("cluster/dist_man.txt")
    starttime=time.time()
    for f in os.listdir(inputdir):
        for line in open(inputdir+"/"+f,"r"):
            if random.random()*100<1:
                info=line.strip().split(",")
                ds.append(float(info[2]))
            solvecnt+=1
            if random.random()*1000000<1:
                outputinfo("sortDist[%s]"%(f),solvecnt,totalcnt,time.time()-starttime)
    ds.sort()
    rat=solvecnt//10000
    sol=0
    fw=open(outputpath,"w")
    for item in ds:
        if sol%rat==0:fw.write("%f\n"%(item))
        sol=sol+1
    fw.close()
def mergePlane(months,planedir):
    fw=open(planedir+"/planeAllNormal.txt","w")
    for mon in months:
        for line in open(planedir+"/planeAllNormal"+mon+".txt","r"):
            info=line.split(",")
            fw.write(mon+"-"+info[0])
            for x in info[1:]:
                fw.write(","+x)
    fw.close()
def loadPlane(planepath):
    global pmap
    pmap=dict()
    index=0
    for line in open(planepath,"r"):
        pmap[line[:line.index(",")]]=index
        index+=1
if __name__=="__main__":
    #mergePlane(months,"plane")
    global clumethod
    months=["201412","201501","201502","201503","201504","201505","201506","201507","201508","201509","201510","201511"]
    for cmeth in ["longest","nearest"]:
        clumethod=cmeth
        for dmeth in ["euc","cos","man"]:
            loadDistFile("cluster/dist_"+dmeth+".txt")
            loadClusterAll(months,"plane")
            planeCluster("cluster/%s_%s.txt"%(cmeth,dmeth))
