import sys
import time
import random
import os
import gzip
from itertools import islice
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
def normalFile(inputpath,outputpath,size):
    minp=dict()
    maxp=dict()
    leng=dict()
    for i in range(2,size):
        minp[i]=None
        maxp[i]=None
    for line in islice(open(inputpath,"r"),1,None):
        info=line.strip().split(",")
        for i in range(2,size):
            if minp[i]==None or minp[i]>float(info[i]):minp[i]=float(info[i])
            if maxp[i]==None or maxp[i]<float(info[i]):maxp[i]=float(info[i])
    for i in range(2,size):
        leng[i]=maxp[i]-minp[i]
    fw=open(outputpath,"w")
    first=True
    for line in open(inputpath,"r"):
        if first:
            first=False
            fw.write(line)
            continue
        info=line.strip().split(",")
        for i in range(2,size):
            if leng[i]==0:info[i]="0.5"
            else:
                info[i]=str((float(info[i])-minp[i])/leng[i])
        for i in range(size):
            fw.write(info[i])
            if i==size-1:fw.write("\n")
            else:fw.write(",")
    fw.close()
if __name__=="__main__":
    montharr=sys.argv[1:]
    totalcnt=len(montharr)
    solvecnt=0
    starttime=time.time()
    for mon in montharr: 
        normalFile("plane"+mon+".txt","normalplane"+mon+".txt",10)
