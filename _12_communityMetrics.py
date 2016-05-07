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
def outputUserDegree(outputpath):
    global pd
    fw=open(outputpath,"w")
    for p in pd:
        fw.write("%d,%d,%d\n"%(p,pd[u][0],pd[u][1]))
    fw.close()
def loadHome(homedir,month):
    global up
    up.clear()
    for line in open(homedir+"/userhome"+month+".txt","r"):
        info=[int(t) for t in line.strip().split(",")]
        up[info[0]]=info[1]
def computeDegree(inputdir,homedir,outputdir,month):
    global pd,up
    pd=dict()
    up=dict()
    #pd[id]=[callpopulation,messpopulation]
    solvecnt=0
    totalcnt=countline(inputpath)
    rate=max(totalcnt/100000,1)
    starttime=time.time()
    loadHome(homedir,month)
    for line in open(intputdir+"/network"+month+".txt","r"):
        #month,u1,u2\tc1,c2
        item=line.strip().split("\t")
        us=[int(t) for t in item[0].split(",")]
        cs=[int(t) for t in item[1].split(",")]
        for u in us[1:]:
            if u not in up:continue
            p=up[u]
            if p not in pd:pd[p]=[0,0]
            for i in range(2):
                if cs[i]>0:pd[p][i]=pd[p][i]+1
        solvecnt=solvecnt+1
        if random.random()*rate<1:
            outputinfo("computeDegree[%s]"%(month),solvecnt,totalcnt,time.time()-starttime)
    outputUserDegree(outputdir+"/degree"+month+".txt")
if __name__=="__main__":
    months=sys.argv[1:]
    for month in months:
        computeDegree("network","home","plane",month)
