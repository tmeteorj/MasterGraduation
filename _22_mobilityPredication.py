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
def loadDistMat(planepath,distpath,interlen):
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
    for line in open(distdisribution,"r"):
        info=line.strip().split(",")
        #dist-top,pop,pre    
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
        pmap[info[0]]=int(info[1])
def computeMoveWeight(month1,month2,outputpath,XA):
    global pmap,wclus,wdist
    ans=list()
    tot=dict()
    for x in wdist:
        tot[x]=0
        for y in wdist:
            try:
                if XA==1:w=math.sqrt(wclus[pmap[month1+"-"+str(x)]][pmap[month2+"-"+str(y)]]*wdist[x][y])
                else:w=(wclus[pmap[month1+"-"+str(x)]][pmap[month2+"-"+str(y)]]+wdist[x][y])/2.0
                ans.append([x,y,w])
                tot[x]+=w
            except:
                pass
    fw=open(outputpath,"w")
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
    for line in open(matmobpath,"r"):
        info=[int(t) for t in  line.strip().split(",")]
        if -1 in info:continue
        if info[0] not in rempop:
            rempop[info[0]]=0
        rempop[info[0]]+=info[2]
    fw=open(outputpath,"w")
    for x in weight:
        for y in weight:
            if x not in rempop or y not in weight[x]:continue
            w=int(rempop[x]*weight[x][y])
            fw.write("%d,%d,%d\n"%(x,y,w))
    fw.close()
def predicationMetrics(matpath,prepath,self):
    cosa=0
    cosb1=0
    cosb2=0
    rl=dict()
    for line in open(matpath,"r"):
        info=[int(t) for t in  line.strip().split(",")]
        if -1 in info:continue
        if not self and info[0]==info[1]:continue
        if info[0] not in rl:rl[info[0]]=dict()
        rl[info[0]][info[1]]=info[2]
        cosb1+=info[2]*info[2]
    for line in open(prepath,"r"):
        info=[int(t) for t in  line.strip().split(",")]
        if not self and info[0]==info[1]:continue
        cosb2+=info[2]*info[2]
        if info[0] in rl and info[1] in rl[info[0]]:cosa+=info[2]*rl[info[0]][info[1]]
    cosb=math.sqrt(cosb1*cosb2)
    return cosa/cosb
if __name__=="__main__":
    loadDistDistribution("predication/distNormalDistribution.txt")
    loadDistMat("PlaneID.txt","PlaneDist.txt",100)
    loadClusterMap("cluster/clus_euc_363.txt")
    months=["201412"]+[str(t) for t in range(201501,201512)]
    fw=open("predication/preMetrics.txt","w")
    starttime=time.time()
    for i in range(11):
        mv=months[i]+"-"+months[i+1]
        loadClusterMat("mobilitymat/innerclustermobility"+mv+".txt")
        computeMoveWeight(months[i],months[i+1],"predication/Xweight"+mv+".txt",1)
        loadMoveWeight("predication/Xweight"+mv+".txt")
        predication("mobilitymat/mat"+mv+".txt","predication/Xpre"+mv+".txt")
        self=predicationMetrics("mobilitymat/mat"+mv+".txt","predication/Xpre"+mv+".txt",True)
        noself=predicationMetrics("mobilitymat/mat"+mv+".txt","predication/Xpre"+mv+".txt",False)
        fw.write("%s,X,%.6f,%.6f\n"%(mv,self,noself))
        computeMoveWeight(months[i],months[i+1],"predication/Aweight"+mv+".txt",2)
        loadMoveWeight("predication/Aweight"+mv+".txt")
        predication("mobilitymat/mat"+mv+".txt","predication/Apre"+mv+".txt")
        self=predicationMetrics("mobilitymat/mat"+mv+".txt","predication/Apre"+mv+".txt",True)
        noself=predicationMetrics("mobilitymat/mat"+mv+".txt","predication/Apre"+mv+".txt",False)
        fw.write("%s,A,%.6f,%.6f\n"%(mv,self,noself))
        outputinfo("predication[%s]"%(mv),i+1,11,time.time()-starttime)
    fw.close()
