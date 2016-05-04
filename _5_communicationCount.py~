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
def communicationGet(monthdir):
    global user
    files=os.listdir(monthdir)
    solvecnt=0
    totalcnt=countlinedir(monthdir)
    starttime=time.time()
    for F in files:
        #20150901.txt
        solvecnt=solvecnt+1
        if len(F)!=12:continue
        for line in open(monthdir+"/"+F,"r"):
            solveOneRecord(line)
            solvecnt=solvecnt+1
            if solvecnt%100000==0:
                outputinfo("communicationGet[%s]"%(monthdir+"/"+F),solvecnt,totalcnt,time.time()-starttime)  
def outputPlaneAttr(outputpath):
    global user
    plane=dict()
    for u in user:
        data=user[u]
        pid=data[0]
        #population  call_out  call_in  call_out_time  call_in_time  call_time  message_out  message_in message_out_time  message_in_time  message_time
        if pid not in plane:plane[pid]=[0,0,0,0,0,0,0,0,0,0,0]
        plane[pid][0]=plane[pid][0]+1
        plane[pid][1]=plane[pid][1]+data[1]
        plane[pid][2]=plane[pid][2]+data[2]
        plane[pid][3]=plane[pid][3]+data[5]
        plane[pid][4]=plane[pid][4]+data[6]
        plane[pid][5]=plane[pid][5]+data[7]
        plane[pid][6]=plane[pid][6]+data[8]
        plane[pid][7]=plane[pid][7]+data[9]
        plane[pid][8]=plane[pid][8]+data[12]
        plane[pid][9]=plane[pid][9]+data[13]
        plane[pid][10]=plane[pid][10]+data[14]
    fw=open(outputpath,"w")
    fw.write("planeID,population,callOut,callIn,callOutTime,callInTime,callTime,messOut,messIn,messOutTime,messInTime,messTime\n")
    for pid in plane:
        first=True
        for x in plane[pid]:
            if first:fw.write(str(x))
            else:fw.write(","+str(x))
            first=False
        fw.write("\n")
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
        communicationGet("i"+m)
        outputinfo("outputPlaneAttr[%s]"%(m),1,1,0)
        outputPlaneAttr("plane/communicationCount"+m+".txt")
        outputinfo("outputPlaneAttr[%s]"%(m),1,1,0)
