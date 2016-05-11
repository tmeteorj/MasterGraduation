import time
import sys
import random
import os
import psutil
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
    if(sizeF>1):count=int(count*sizeF)
    f.close()
    return count
def loadCom(inputpath,idx):
    global usercom
    for line in open(inputpath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        if info[0] not in usercom:usercom[info[0]]=[None,None,None]
        usercom[info[0]][idx]=info[1]
def getNMI(ida,idb,idr):
    global usercom,result
    solvecnt=0
    totalcnt=len(usercom)
    starttime=time.time()
    last=None
    for item in sorted(usercom.items(),key=lambda arg:arg[1][0]):
        if last==None:
            last=item[1][0]
            pa=dict()
            pb=dict()
            pab=dict()
            ct=0.0
        if last!=item[1][0]:
            ha=0.0
            hb=0.0
            mi=0.0
            for x in pa:ha-=pa[x]/ct*math.log(pa[x]/ct)
            for y in pb:hb-=pb[y]/ct*math.log(pb[y]/ct)
            for xy in pab:
                a=[int(t) for t in xy.split(",")]
                mi+=pab[xy]/ct*math.log(pab[xy]*ct/(pa[a[0]]*pb[a[1]]))
            if mi>0 or ha>0 or hb>0:
                nmi=2*mi/(ha+hb)
                if last not in result:result[last]=[0,0,0]
                result[last][idr]=nmi
            last=item[1][0]
            pa.clear()
            pb.clear()
            pab.clear()
            ct=0.0
        pa[item[1][ida]]=1.0 if item[1][ida] not in pa else pa[item[1][ida]]+1.0
        pb[item[1][idb]]=1.0 if item[1][idb] not in pb else pb[item[1][idb]]+1.0
        xy="%d,%d"%(item[1][ida],item[1][idb])
        pab[xy]=1.0 if xy not in pab else pab[xy]+1.0
        ct=ct+1.0
        solvecnt=solvecnt+1
        if random.random()*10000<1:
            outputinfo("getNMI(%d,%d,%d)"%(ida,idb,idr),solvecnt,totalcnt,time.time()-starttime)
    ha=0.0
    hb=0.0
    mi=0.0
    for x in pa:ha-=pa[x]/ct*math.log(pa[x]/ct)
    for y in pb:hb-=pb[y]/ct*math.log(pb[y]/ct)
    for xy in pab:
        a=[int(t) for t in xy.split(",")]
        mi+=pab[xy]/ct*math.log(pab[xy]*ct/(pa[a[0]]*pb[a[1]]))
    if mi>0 or ha>0 or hb>0:
        nmi=2*mi/(ha+hb)
        if last not in result:result[last]=[0,0,0]
        result[last][idr]=nmi
def getEntropy(idx,idr):
    global usercom,result
    solvecnt=0
    totalcnt=len(usercom)
    starttime=time.time()
    last=None
    for item in sorted(usercom.items(),key=lambda arg:arg[1][0]):
        if last==None:
            last=item[1][0]
            p=dict()
            ct=0.0
        if last!=item[1][0]:
            e=0.0
            for x in p:e-=p[x]/ct*math.log(p[x]/ct)
            if last not in result:result[last]=[0,0,0]
            result[last][idr]=e
            last=item[1][0]
            p.clear()
            ct=0.0
        p[item[1][idx]]=1.0 if item[1][idx] not in p else p[item[1][idx]]+1.0
        ct=ct+1.0
        solvecnt=solvecnt+1
        if random.random()*10000<1:
            outputinfo("getEntropy(%d,%d)"%(idx,idr),solvecnt,totalcnt,time.time()-starttime)
    e=0.0
    for x in p:e-=p[x]/ct*math.log(p[x]/ct)
    if last not in result:result[last]=[0,0,0]
    result[last][idr]=e
def getCommunityNumber(outputpath):
    global usercom
    comcnt=dict()
    last=None
    for item in sorted(usercom.items(),key=lambda arg:arg[1][0]):
        if last==None:
            last=item[1][0]
            ct=[set(),set()]
        if last!=item[1][0]:
            comcnt[last]=[len(ct[0]),len(ct[1])]
            last=item[1][0]
            ct[0].clear()
            ct[1].clear()
        ct[0].add(item[1][1])
        ct[1].add(item[1][2])
    fw=open(outputpath,"w")
    for x in sorted(comcnt.items(),key=lambda arg:arg[0]):
        fw.write("%d,%d,%d\n"%(x[0],x[1][0],x[1][1]))
    fw.close()
def outputMetrics(outputpath):
    global result
    fw=open(outputpath,"w")
    for x in sorted(result.items(),key=lambda arg:arg[0]):
        fw.write("%d,%.6f,%.6f,%.6f\n"%(x[0],x[1][0],x[1][1],x[1][2]))
        #fw.write("%d,%.6f\n"%(x[0],x[1][0]))
    fw.close()
if __name__=="__main__":
    global usercom,result
    usercom=dict()
    result=dict()
    months=sys.argv[1:] 
    for month in months:
        usercom.clear()
        result.clear()
        loadCom("home/userhome"+month+".txt",0)
        loadCom("communitySingle/nodeCall"+month+".txt",1)
        loadCom("communitySingle/nodeMess"+month+".txt",2)
        #call-mess
        getNMI(1,2,0)
        getEntropy(1,1)
        getEntropy(2,2)
        outputMetrics("plane/communityMetrics"+month+".txt")
        #getCommunityNumber("plane/comcnt"+month+".txt")

