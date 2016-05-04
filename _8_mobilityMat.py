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
def computeMobilityMat(inputdir,outputdir,month):
    mat=dict()
    mat[-1]=dict()
    for line in open(inputdir+"/new"+month,"r"):
        info=line.strip().split(",")
        u=int(info[1])
        mat[-1][u]=1 if u not in mat[-1] else mat[-1][u]+1
    for line in open(inputdir+"/remove"+month,"r"):
        info=line.strip().split(",")
        u=int(info[1])
        mat[u][-1]=1 if -1 not in mat[u] else mat[u][-1]+1
    for line in open(inputdir+"/move"+month,"r"):
        info=line.strip().split(",")
        ua=int(info[1])
        ub=int(info[2])
        mat[ua][ub]=1 if ub not in mat[ua] else mat[ua][ub]+1
    for line in open(inputdir+"/stay"+month,"r"):
        info=line.strip().split(",")
        ua=int(info[1])
        mat[ua][ua]=1 if ua not in mat[ua] else mat[ua][ua]+1
    fw=open(outputdir+"/mat"+month,"w")
    for ua in mat:
        for ub in mat[ua]:
            fw.write("%d,%d,%d\n"%(ua,ub,mat[ua][ub]))
    fw.close()
if __name__=="__main__":
    montharr=sys.argv[1:]
    totalcnt=len(montharr)-1
    solvecnt=0
    starttime=time.time()
    for mo in range(totalcnt):
        fn=montharr[mo]+"-"+montharr[mo+1]+".txt"
        computeMobilityMat("mobility","mobilitymat",fn)
        solvecnt=solvecnt+1
        outputinfo("mobilitymat[%s]"%(fn),solvecnt,totalcnt,time.time()-starttime)
