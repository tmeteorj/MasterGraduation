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
    global distmethod
    if distmethod=="euc":
        ds=0.0
        for p in zip(a,b):
            ds+=(p[0]-p[1])**2
        return ds
    elif distmethod=="cos":
        top=0.0
        bota=0.0
        botb=0.0
        for p in zip(a,b):
            top+=p[0]*p[1]
            bota+=p[0]*p[0]
            botb+=p[1]*p[1]
        bot=math.sqrt(bota)*math.sqrt(botb)
        return top/bot
    elif distmethod=="man":
        ds=0.0
        for p in zip(a,b):
            ds+=math.abs(p[0]-p[1])
        return ds
def loadPlane(planepath):
    global pmap
    pmap=list()
    for line in open(planepath,"r"):
        info=line.strip().split(",")
        pmap.append([info[0],[float(t) for t in info[1:]],-1])
def initKMeans(K):
    global clu,pmap
    clu=[None]*K
    rid=int(random.random()*len(pmap))
    clu[0]=[None]*3
    clu[0][0]=[float(t) for t in pmap[rid][1]]
    clu[0][1]=0
    clu[0][2]=[0]*len(pmap[rid][1])
    for i in range(1,K):
        maxds=-1
        maxv=-1
        for x in pmap:
            minds=100.0
            for j in range(i):
                ds=distance(clu[j][0],x[1])
                if ds<minds:minds=ds
            if maxds<minds:
                maxds=minds
                maxv=x[1]
        clu[i]=[None]*3
        clu[i][0]=[float(t) for t in maxv]
        clu[i][1]=0
        clu[i][2]=[0]*len(maxv)
def KMeans(K,outputpath):
    global clu,pmap
    starttime=time.time()
    flag=True
    for itertime in range(100):
        if itertime==0:initKMeans(K)
        else:
            for item in clu:
                item[0]=[x/item[1] for x in item[2]]
                item[1]=0
                item[2]=[0]*len(item[0])
        flag=False
        for p im pmap:
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
                clu[minid][2]+=x
            clu[minid][1]+=1
        if not flag:break
        outputinfo("KMeans(%d,%s)"%(K,outputpath),itertime+1,100,time.time()-starttime)
    fw=open(outputpath,"w")
    for p in pmap:
        fw.write("%s,%d\n"%(p[0],p[2]))
    fw.close()
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
def mergePlane(months,planedir):
    fw=open(planedir+"/planeAllNormal.txt","w")
    for mon in months:
        for line in open(planedir+"/planeAllNormal"+mon+".txt","r"):
            info=line.split(",")
            fw.write(mon+"-"+info[0])
            for x in info[1:]:
                fw.write(","+x)
    fw.close()
if __name__=="__main__":
    global distmethod
    loadPlane("plane/planeAllNormal.txt")
    for K in [5,10,20,50,100,200,500,1000]:
        for method in ["euc","cos","man"]:
            distmethod=method
            KMeans(K,"cluster/clus_%s_%d.txt"%(method,K))
