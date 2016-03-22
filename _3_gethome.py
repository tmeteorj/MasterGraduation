import time
import random
import os
import gzip
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
    global basemap,user
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
                if info[2] not user:user[info[2]]=dict()
                user[info[2]][plane]=1 if plane not in user[info[2]] else user[info[2]][plane]+1
        solvecnt=solvecnt+1
        h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
        print("gethome: %s, completed: %d/%d=%.4f%%, remain: %02d:%02d:%02d"%(recorddir,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    fw=open(homepath,"w")
    for u in user:
        maxcnt=0
        maxloc="null"
        for pid in user[u]:
            cnt=user[u][pid]
            if cnt>maxcnt:
                maxcnt=cnt
                maxloc=pid
        fw.write("%s,%s,%d\n"%(u,maxloc,maxcnt))
    fw.close()
if __name__=="__main__":
    loadbase("BasePlaneSimple.csv")
    for month in ["201412","201501","201502","201503","201504"]:
        gethome("i"+month,"home/userhome"+month+".txt")

