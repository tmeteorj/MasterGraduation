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
def adduser(name):
    global hashuser,usercnt
    if name in hashuser:return hashuser[name]
    else:
        hashuser[name]=usercnt
        usercnt=usercnt+1
        return usercnt-1
def getrecord(inputdir,outputdir,userpath):
    global hashuser,usercnt
    files=os.listdir(inputdir)
    files.sort()
    hashuser.clear()
    usercnt=0
    totalcnt=len(files)
    solvecnt=0
    starttime=time.time()
    fw=dict()
    for f in files:
        for line in gzip.open(inputdir+"/"+f,"rb"):
            info=line.decode("utf-8").strip().split(",")
	    day=info[1][0:8]
	    if day not in fw:
                fw[day]=open(outputdir+"/"+day+".txt","w")
                fw[day+"traj"]=open(outputdir+"/"+day+"traj.txt","w")
            if info[0] in {"1","3","6","7"} and info[4]!="da39a3ee5e6b4b0d3255bfef95601890afd80709" and info[6]!="da39a3ee5e6b4b0d3255bfef95601890afd80709":
                ua=adduser(info[4])
                ub=adduser(info[6])
                fw[day].write("%s,%s,%s-%s,%d,%d\n"%(info[0],info[1][0:17],info[2],info[3],ua,ub))
            if info[0]=="13" and info[4]!="da39a3ee5e6b4b0d3255bfef95601890afd80709":
                ua=adduser(info[4])
                fw[day+"traj"].write("%s,%s-%s,%d\n"%(info[1][0:17],info[2],info[3],ua))
        solvecnt+=1
        h,m,s=timeEvaluation(solvecnt,totalcnt,time.time()-starttime)
        print("getrecord[%s] usercnt: %d, completed: %d/%d -> %.3f%%, remain %02d:%02d:%02d\n"%(inputdir,usercnt,solvecnt,totalcnt,solvecnt*100.0/totalcnt,h,m,s))
    for name in fw:fw[name].close()
    fw=open(userpath,"w")
    for u in hashuser:
        fw.write("%s,%d\n"%(u,hashuser[u]))
    fw.close()
def deletefiles(inputdir):
    for name in os.listdir(inputdir):
        os.remove(inputdir+"/"+name)
if __name__=="__main__":
    hashuser=dict()
    month=["201412","201501","201502","201503","201504"]
    for m in month:
        getrecord(m,"i"+m,"hash"+m+".txt")
        deletefiles(m)