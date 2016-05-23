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
def distance(a,b):
    ds=0.0
    for p in zip(a,b):
        ds+=(p[0]-p[1])**2
    return ds
def loadPlane(planepath):
    global pmap,pid
    pmap=list()
    pid=dict()
    idx=0
    for line in open(planepath,"r"):
        info=line.strip().split(",")
        pmap.append([info[0],[float(t) for t in info[1:]],-1])
        pid[info[0]]=idx
        idx+=1
def initKMeans(K):
    outputinfow("start init KMeans(%d)"%(K))
    global clu,pmap
    clu=[None]*K
    rid=int(random.random()*len(pmap))
    clu[0]=[None]*3
    clu[0][0]=[float(t) for t in pmap[rid][1]]
    clu[0][1]=0
    clu[0][2]=[0]*len(pmap[rid][1])
    solvecnt=0
    totalcnt=999*100*500
    starttime=time.time()
    lasttime=time.time()
    psize=len(pmap)
    for i in range(1,K):
        maxds=-1
        maxv=-1
        for t in range(100):
            x=pmap[int(random.random()*psize)]
            minds=100.0
            for j in range(i):
                ds=distance(clu[j][0],x[1])
                if ds<minds:minds=ds
            if maxds<minds:
                maxds=minds
                maxv=x[1]
            solvecnt+=i
            if time.time()-lasttime>=10:
                lasttime=time.time()
                outputinfo("init KMeans",solvecnt,totalcnt,lasttime-starttime)
        if maxds==0:
            print("MDZZ")
            sys.exit(-1)        
        clu[i]=[None]*3
        clu[i][0]=[float(t) for t in maxv]
        clu[i][1]=0
        clu[i][2]=[0]*len(maxv)
    outputinfow("completed init KMeans(%d)"%(K))
def writeClu(outputpath):
    global clu
    fw=open(outputpath,"w")
    for c in clu:
        flag=False
        for x in c[0]:
            if flag:fw.write(",")
            fw.write("%f"%(x))
            flag=True
        fw.write("\n")
    fw.close()
def loadClu(K,inputpath):
    global clu
    clu=[None]*K
    rid=int(random.random()*len(pmap))
    lines=open(inputpath,"r").readlines()
    tot=len(lines)
    for i in range(K):
        clu[i]=[[float(t) for t in lines[(i+rid)%tot].strip().split(",")],0,[0]*19]
def KMeans(K,outputpath,maxiter):
    global clu,pmap
    flag=True
    for itertime in range(maxiter):
        if itertime==0:
            loadClu(K,"KMeansInit.txt")
            starttime=time.time()
            lasttime=0
        else:
            for item in clu:
                item[0]=[x/item[1] for x in item[2]]
                item[1]=0
                item[2]=[0]*len(item[0])
        flag=False
        for p in pmap:
            minds=100.0
            minid=-1
            for c,cid in zip(clu,range(K)):
                ds=distance(c[0],p[1])
                if ds<minds:
                    minds=ds
                    minid=cid
            if p[2]!=minid:
                flag=True
                p[2]=minid
            for x,xid in zip(p[1],range(len(p[1]))):
                clu[minid][2][xid]+=x
            clu[minid][1]+=1
        if not flag:
            outputinfow("Arrived to the stable point after %d iterations"%(itertime+1))
            break
        if time.time()-lasttime>=5:
            lasttime=time.time()
            outputinfo("KMeans(%d,%s)"%(K,outputpath),itertime+1,maxiter,lasttime-starttime)
    fw=open(outputpath,"w")
    for p in sorted(pmap,key=lambda arg:arg[2]):
        fw.write("%s,%d\n"%(p[0],p[2]))
    fw.close()
def computeMetrics(K,clusterpath,size):
    global pmap,pid
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
            tot=len(ls)
            cen[last]=[0]*size
            for x in ls:
                data=pmap[pid[x]][1]
                for y,yid in zip(data,range(size)):
                    cen[last][yid]+=y
            cen[last]=[float(t)/tot for t in cen[last]]
            res=0.0
            for x in ls:
                res+=distance(pmap[pid[x]][1],cen[last])
            avg[last]=math.sqrt(res/tot)
            last=info[1]
            ls=list()
        ls.append(info[0])
    res=0
    tot=len(ls)
    cen[last]=[0]*size
    for x in ls:
        data=pmap[pid[x]][1]
        for y,yid in zip(data,range(size)):
            cen[last][yid]+=y
    cen[last]=[float(t)/tot for t in cen[last]]
    for x in ls:
        res+=distance(pmap[pid[x]][1],cen[last])
    avg[last]=math.sqrt(res/tot)
    dbi=0.0
    for i in range(K):
        mx=0.0
        for j in range(K):
            if i==j:continue
            mx=max(mx,(avg[i]+avg[j])/math.sqrt(distance(cen[i],cen[j])))
        dbi+=mx
    dbi=dbi/float(K)
    return dbi
if __name__=="__main__":
    loadPlane("plane/planeAllNormal.txt")
    #initKMeans(1000)
    #writeClu("KMeansInit.txt")
    fw=open("clusterMetrics.txt","w")
    KS=list(range(2,21))+[t*10 for t in range(3,100)]
    for K in KS:
        KMeans(K,"cluster/clus_euc_%d.txt"%(K),300)
        dbi=computeMetrics(K,"cluster/clus_euc_%d.txt"%(K),19)
        print("%d->%.5f\n"%(K,dbi))
        fw.write("%d,%.5f\n"%(K,dbi))
        fw.flush()
    fw.close()
        
