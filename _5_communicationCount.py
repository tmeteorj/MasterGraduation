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
def timediff(t1,t2):
    d1=datetime.datetime.strptime(t1,"%Y%m%d %H:%M:%S")
    d2=datetime.datetime.strptime(t2,"%Y%m%d %H:%M:%S")
    return (d2-d1).total_seconds()
def latestTime(t1,t2):
    if t1==None:return t2
    if t2==None:return t1
    if timediff(t1,t2)<0:return t2
    else:return t1
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
def countlinedir(dirpath):
    files=os.listdir(dirpath)
    ave=-1
    cnt=0
    for f in files:
        if len(f)!=12:continue
        p=dirpath+"/"+f
        if ave==-1:
            ave=1.0*countline(p)/os.path.getsize(p)
        cnt=cnt+os.path.getsize(p)
    return cnt*ave
def loadBasicInfo(monthpath):
    global user
    user.clear()
    pop=dict()
    for line in open(monthpath,"r"):
        #user,plane,cnt
        info=line.strip().split(",")
        #belong
        #call_out    call_in    last_call_out    last_call_in   total_call_out_time  total_call_in_time total_time
        #message...
        user[info[0]]=[info[1],0,0,None,None,0,0,0,0,0,None,None,0,0,0]
def solveOneRecord(record):
    global user
    #type,time,big-small,ua,ub
    info=record.strip().split(",")
    if info[3] not in user:return
    ntime=info[1]
    data=user[info[3]]
    if info[0] in ["1","3"]:ad=1
    elif info[0] in ["6","7"]:ad=8
    else:return
    if info[0] in ["1","6"]:
        data[ad]=data[ad]+1
        prevtime=data[ad+2]
        if prevtime!=None:
            d=timediff(prevtime,ntime)
            data[ad+4]=data[ad+4]+d
        data[ad+2]=ntime
    elif info[0] in ["3","7"]:
        data[ad+1]=data[ad+1]+1
        prevtime=data[ad+3]
        if prevtime!=None:
            d=timediff(prevtime,ntime)
            data[ad+5]=data[ad+5]+d
        data[ad+3]=ntime
    ltime=latestTime(data[ad+2],data[ad+3])
    if ltime!=None:
        tottime=timediff(ltime,ntime)
        data[ad+6]=data[ad+6]+tottime
def userBehaviorGet(monthdir,userpath):
    global user
    files=os.listdir(monthdir)
    solvecnt=0
    totalcnt=len(files)
    starttime=time.time()
    for F in files:
        for line in open(monthdir+"/"+F,"r"):
            solveOneRecord(line)
            if random.random()*1000000<1:
                print("[%s] solving file %s\n"%(gettime(),F))
        solvecnt=solvecnt+1
        outputinfo("communicationGet[%s]"%(monthdir+"/"+F),solvecnt,totalcnt,time.time()-starttime)
    fw=open(userpath,"w")
    for u in user:
        fw.write("%s,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n"%(str(u),user[u][0],user[u][1],user[u][2],user[u][5],user[u][6],user[u][7],user[u][8],user[u][9],user[u][12],user[u][13],user[u][14]))
    fw.close()
def updateAveInter(arr,tot,cnt):
    if cnt>1:
        arr[0]+=float(tot)/(cnt-1.0)
        arr[1]+=1
    return arr
def makePlaneStr(x):
    if x[1][0]==0:
        return str(x[0])+",0,0,0,0,0,0,0,0,0,0,0"
    ans="%d,%d,%.2f,%.2f"%(x[0],x[1][0],x[1][1]*1.0/x[1][0],x[1][2]*1.0/x[1][0])
    for i in range(3,6):
        if x[1][i][1]==0:
            ans=ans+",%.2f"%(x[1][i][0]/x[1][i][1])
        else:
            ans=ans+",0"
    ans=ans+",%.2f,%.2f"%(x[1][6]*1.0/x[1][0],x[1][7]*1.0/x[1][0])
    for i in range(8,11):
        if x[1][i][1]==0:
            ans=ans+",%.2f"%(x[1][i][0]/x[1][i][1])
        else:
            ans=ans+",0"
    return ans
def planeBehaviorGet(userdir,planedir):
    files=os.listdir(userdir)
    for f in files:
        month=f[f.index("2"):f.index(".")]
        plane=dict()
        for line in open(userdir+"/"+f,"r"):
            u=[int(t) for t in line.strip().split(",")]
            pid=u[1]
            if pid not in plane:plane[pid]=[0,0,0,[0,0],[0,0],[0,0],0,0,[0,0],[0,0],[0,0]]
            plane[pid][0]+=1
            plane[pid][1]+=u[2]
            plane[pid][2]+=u[3]
            plane[pid][3]=updateAveInter(plane[pid][3],u[4],u[2])
            plane[pid][4]=updateAveInter(plane[pid][4],u[5],u[3])
            plane[pid][5]=updateAveInter(plane[pid][5],u[6],u[2]+u[3])
            plane[pid][6]+=u[7]
            plane[pid][7]+=u[8]
            plane[pid][8]=updateAveInter(plane[pid][8],u[9],u[7])
            plane[pid][9]=updateAveInter(plane[pid][9],u[10],u[8])
            plane[pid][10]=updateAveInter(plane[pid][10],u[11],u[7]+u[8])
        fw=open(planedir+"/communicationCount"+month+".txt","w")
        fw.write("PID,Population,CallOutCnt,CallInCnt,CallOutInter,CallInInter,CallInter,MessOutCnt,MessInCnt,MessOutInter,MessInInter,MessInter\n")
        for x in sorted(plane.items(),key=lambda arg:arg[0]):
            fw.write("%s\n"%(makePlaneStr(x))
        fw.close()
if __name__=="__main__":
    global user
    user=dict()
    month=sys.argv[1:]
    solvecnt=0
    totalcnt=len(month)
    starttime=time.time()
    for m in month:
        loadBasicInfo("home/userhome"+m+".txt")
        userBehaviorGet("DataCom/com"+m,"user/behavior"+m+".txt")
    planeBehaviorGet("user","plane")
