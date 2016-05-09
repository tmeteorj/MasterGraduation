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
def extractCitizen(homedir,inputdir,outputdir):
    files=os.listdir(inputdir)
    solvecnt=0
    totalcnt=len(files)
    starttime=time.time()
    for f in files:
        fw=open(outputdir+"/"+f,"w")
        user=set()
        for line in open(homedir+"/"+f.replace("net","userhome"),"r"):
            user.add(line[:line.index(",")])
        for line in open(inputdir+"/"+f,"r"):
            info=line.strip().split("\t")
            us=info[0].strip().split(",")
            if us[1] not in user or us[2] not in user:continue
            fw.write(line)
        fw.close()
        solvecnt=solvecnt+1
        outputinfo("ectractCitizen[%s]"%(f),solvecnt,totalcnt,time.time()-starttime)
if __name__=="__main__":
    months=sys.argv[1:]
    for month in months:
        extractCitizen("home","network","networkCitizen")
    #getSocialData("network","community","home")
