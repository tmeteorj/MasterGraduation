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
def loadbase(inputpath):
    global basemap
    basemap=dict()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        basemap[info[0]]=info[3]
def gethome(recorddir,homepath):
    global basemap
    user=dict()
    files=os.listdir(recorddir)
    files.sort()
    solvecnt=0
    totalcnt=len(files)/2
    starttime=time.time()
    for name in files:
        if name.find("traj.txt")==-1:continue
        for line in open(recorddir+"/"+name,"r"):
            #time,big-small,userid
            info=line.strip().split(",")
            hr=int(info[0][9:11])
            if (hr>=21 or hr<7) and info[1] in basemap:
                plane=basemap[info[1]]
                if info[2] not in user:user[info[2]]=dict()
                user[info[2]][plane]=1 if plane not in user[info[2]] else user[info[2]][plane]+1
        solvecnt=solvecnt+1
        outputinfo("gethome[%s]"%(recorddir),solvecnt,totalcnt,time.time()-starttime)
    result=dict()
    for u in user:
        maxcnt=0
        maxloc="null"
        for pid in user[u]:
            cnt=user[u][pid]
            if cnt>maxcnt:
                maxcnt=cnt
                maxloc=pid
        result[u+","+maxloc]=maxcnt
    fw=open(homepath,"w")
    for x in sorted(result.items(),key=lambda arg:arg[1]):
        fw.write("%s,%d\n"%(x[0],x[1]))
    fw.close()
def removeuser(homepath,realhome,thred):
    fw=open(realhome,"w")
    for line in open(homepath,"r"):
        info=line.strip().split(",")
        if int(info[-1])>=thred:fw.write("%s,%s\n"%(info[0],info[1]))
    fw.close()
def decodeuser(usermappath,realhome,codehome):
    hashuser=dict()
    for line in open(usermappath,"r"):
        info=line.strip().split(",")
        hashuser[info[1]]=info[0]
    fw=open(codehome,"w")
    for line in open(realhome,"r"):
        info=line.strip().split(",")
        fw.write("%s,%s\n"%(hashuser[info[0]],info[1]))
    fw.close()
if __name__=="__main__":
    loadbase("BasePlaneSimple.csv")
    montharr=sys.argv[1:]
    for month in montharr:
        gethome("i"+month,"home/userhome"+month+".txt")
        print("Before remove and decode users")
        removeuser("home/userhome"+month+".txt","home/realhome"+month+".txt",70)
        decodeuser("hashuser/hash"+month+".txt","home/realhome"+month+".txt","home/originrealhome"+month+".txt")
        print("After remove and decode users")
