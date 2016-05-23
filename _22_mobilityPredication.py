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
def loadDistmat(planepath,distpath,interlen):
    global wdist,distpre
    wdist=dict()
    pid=[int(t.strip()) for t in open(planepath,"r")]
    for ida,line in zip(pid,open(distpath,"r")):
        ds=[float(t) for t in line.strip().split(",")]
        wdist[ida]=dict()
        for idb,x in zip(pid,ds):
            ix=int(x)//interlen
            wdist[ida][idb]=distpre[ix][1]
def loadDistDistribution(distdisribution):
    global distpre
    distpre=list()
    for line in open(distdistribution,"r"):
        info=line.strip().split(",")
        #dist-mid,pop,pre    
        distpre.append([int(info[0]),float(info[2])])
def loadClusterMat(clustermatpath):
    global wclus
    wclus=dict()
    for line in open(clustermatpath,"r"):
        #a,b,pop,pre
        info=line.strip().split(",")
        cid=[int(t) for t in info[:2]]
        if cid[0] not in wclus:wclus[cid[0]]=dict()
        wclus[cid[0]][cid[1]]=float(info[3])
def loadClusterMap(clustermappath):
    global pmap
    pmap=dict()
    for line in open(clustermappath,"r"):
        info=line.strip().split(",")
        idp=int(info[0][info[0].index("-")+1:])
        pmap[idp]=int(info[1])
def moveWeight(outputpath):
    global pmap,wclus,wdist
    ans=list()
    tot=dict()
    for x in pmap:
        tot[x]=0
        for y in pmap:
            w=math.sqrt(wclus[pmap[x]][pmap[y]]*wdist[x][y]])
            ans.append([x,y,w])
            tot[x]+=w
    fw=open(outputpath,"w"):
    for item in ans:
        if item[2]>0:fw.write("%d,%d,%.6f\n"%(item[0],item[1],item[2]/tot[item[0]]))
    fw.close()
def loadMoveWeight(weightpath):
    global weight
    weight=dict()
    for line in open(weightpath,"r"):
        info=line.strip().split(",")
        pid=[int(t) for t in info[:2]]
        if pid[0] not in weight:weight[pid[0]]=dict()
        weight[pid[0]][pid[1]]=float(info[2])
def predication(matmobpath,outputpath):
    global weight
    rempop=dict()
    rl=dict()
    cosa=0
    cosb1=0
    cosb2=0
    for line in open(matmobpath,"r"):
        info=[int(t) for t in  line.strip().split(",")]
        if info[0] not in rempop:
            rempop[info[0]]=0
            rl[info[0]]=dict()
        rempop[info[0]]+=info[2]
        rl[info[0]][info[1]]=info[2]
        cosb1+=info[2]*info[2]
    fw=open(outputpath,"w")
    for x in weight:
        for y in weight:
            w=int(rempop[x]*weight[x][y])
            fw.write("%d,%d,%d\n"%(x,y,w))
            cosb2+=w*w
            if x rl and y in rl[x]:
                cosa+=w*rl[x][y]
    fw.close()
    cosb=math.sqrt(cosb1*cosb2)
    return cosa/costb
if __name__=="__main__":
    loadDistMat("PlaneInfo.txt","PlaneDist.txt")
    computeMobPop("mobilitymat/matAll.txt","predication/distDistribution.txt")
    computeDistPop("predication/distDistribution.txt","predication/distFormatDistribution.txt",32000,500)
