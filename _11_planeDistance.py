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
def sortBasePointMap(basepointpath,keypointpath):
    res=dict()
    for line in open(basepointpath,"r"):
        info=line.strip().split(",")
        res[info[0]]=int(info[1])
    fw1=open(basepointpath,"w")
    fw2=open(keypointpath,"w")
    lastk=-1
    for x in sorted(res.items(),key=lambda arg:arg[1]):
        fw1.write("%s,%d\n"%(x[0],x[1]))
        if lastk!=-1 and lastk!=x[1]:
            fw2.write("%d\n",lastk)
        lastk=x[1]
    fw1.close()
    fw2.close()
if __name__=="__main__":
    sortBasePointMap("BasePointMap.txt","KeyPoint.txt")
