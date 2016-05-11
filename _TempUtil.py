import sys
import time
import random
import os
import gzip
import datetime
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
def removeTime(inputdir,outputdir):
    files=os.listdir(inputdir)
    solvecnt=0
    totalcnt=len(files)
    starttime=time.time()
    for f in files:
        fw=open(outputdir+"/"+f,"w")
        for line in open(inputdir+"/"+f,"r"):
            u=line.strip().split(",")
            fw.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(u[0],u[1],u[2],u[3],u[6],u[7],u[8],u[9],u[10],u[13],u[14],u[15]))
        fw.close()
if __name__=="__main__":
    removeTime("userold","user")
