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
    err=set()
    for f in files:
        try:
            for line in gzip.open(inputdir+"/"+f,"rb"):
                info=line.decode("utf-8").strip().split(",")
                day=info[1][0:8]
                if day[0:2]!="20" or info[4]=="da39a3ee5e6b4b0d3255bfef95601890afd80709":continue
                if day not in fw:
                    fw[day]=open(outputdir+"/"+day+".txt","w")
                    fw[day+"traj"]=open(outputdir+"/"+day+"traj.txt","w")
                    fw[day+"move"]=open(outputdir+"/"+day+"move.txt","w")
                if info[0] in {"1","3","6","7"} or info[6]!="da39a3ee5e6b4b0d3255bfef95601890afd80709":
                    ua=adduser(info[4])
                    ub=adduser(info[6])
                    fw[day].write("%s,%s,%s-%s,%d,%d\n"%(info[0],info[1][0:17],info[2],info[3],ua,ub))
                if info[0]=="13":
                    ua=adduser(info[4])
                    fw[day+"traj"].write("%s,%s-%s,%d\n"%(info[1][0:17],info[2],info[3],ua))
                if info[0]=="12":
                    ua=adduser(info[4])
                    fw[day+"move"].write("%s,%s-%s,%d\n"%(info[1][0:17],info[2],info[3],ua))
            solvecnt+=1
            outputinfo("getrecord[%s]"%(inputdir),solvecnt,totalcnt,time.time()-starttime)
        except:
            err.add(f)
    for name in fw:fw[name].close()
    fw=open(userpath,"w")
    starttime=time.time()
    solvecnt=0
    totalcnt=usercnt
    for u in hashuser:
        fw.write("%s,%d\n"%(u,hashuser[u]))
        solvecnt+=1
        if(solvecnt%10000==0):
            outputinfo("writeuser[%s]"%(inputdir),solvecnt,totalcnt,time.time()-starttime)
    fw.close()
    return err
def deletefiles(inputdir,err):
    for name in os.listdir(inputdir):
        if name not in err:os.remove(inputdir+"/"+name)
if __name__=="__main__":
    global hashuser
    hashuser=dict()
    month=sys.argv[1:]
    for m in month:
        err=getrecord(m,"i"+m,"hashuser/hash"+m+".txt")
        deletefiles(m,err)
        if len(err)>0:
            fw=open("err_log.txt","a")
            for item in err:
                fw.write("[Error %s]: In _2_infoExtract.py, file %s can't be read\n"%(gettime(),item))
            fw.close()
            
