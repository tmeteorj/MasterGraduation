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
def getInfomapData(inputdir,outputdir,month):
    #month,u1,u2    call,mess
    tmpc=open("tmpcall.txt","w")
    tmpm=open("tmpmess.txt","w")
    hsc=dict()
    hsm=dict()
    nc=0
    nm=0
    nce=0
    nme=0
    solvecnt=0
    totalcnt=countline(inputpath)
    rate=max(totalcnt/100000,1)
    starttime=time.time()
    for line in open(inputdir+"/network"+month+".txt","r"):
        item=line.strip().split("\t")
        us=[int(t) for t in item[0]]
        cs=[int(t) for t in item[1]]
        if cs[0]>0:
            u=[0,0]
            for i in range(2):
                if us[i] not in hsc:
                    nc=nc+1
                    hsc[us[i]]=nc
                u[i]=hsc[us[i]]
            nce=nce+1
            tmpc.write("%d %d %d\n"%(u[0],u[1],cs[0]))
        if cs[1]>0:
            u=[0,0]
            for i in range(2):
                if us[i] not in hsm:
                    nm=nm+1
                    hsm[us[i]]=nm
                u[i]=hsm[us[i]]
            nme=nme+1
            tmpm.write("%d %d %d\n"%(u[0],u[1],cs[1]))
        solvecnt=solvecnt+1
        if random.random()*rate<1:
            outputinfo("getInfoMapData[%s]"%(month),solvecnt,totalcnt,time.time()-starttime)
    tmpc.close()
    tmpm.close()
    fwc=open(outputdir+"/imCall"+str(month)+".net","w")
    fwc.write("*Vertices %d\n"%(nc))
    for x in sorted(hsc.items(),key=lambda arg:arg[1]):
        fwc.write("%d \"%d\"\n"%(x[1],x[0]))
    fwc.write("*Edges %d\n"%(nce))
    for line in open("tmpcall.txt","r"):
        fwc.write(line)
    fwc.close()
    fwm=open(outputdir+"/imMess"+str(month)+".net","w")
    fwm.write("*Vertices %d\n"%(nm))
    for x in sorted(hsm.items(),key=lambda arg:arg[1]):
        fwm.write("%d \"%d\"\n"%(x[1],x[0]))
    fwm.write("*Edges %d\n"%(nme))
    for line in open("tmpmess.txt","r"):
        fwm.write(line)
    fwm.close()
    os.remove("tmpmess.txt")
    os.remove("tmpcall.txt")
def loadUser(inputpath):
    global us
    us.clear()
    for line in open(inputpath,"r"):
        info=line.strip().split(",")
        us[int(info[0])]=int(info[1])
def getSocialData(inputdir,outputdir,homedir):
    global us
    us=dict()
    files=os.listdir(inputdir)
    solvecnt=0
    totalcnt=len(files)
    starttime=time.time()
    for f in files:
        mon=f[f.index("2"):f.index(".")]
        loadUser(homedir+"/userhome"+mon+".txt")
        fw=open(outputdir+"/"+f.replace(".tree",".txt"),"w")
        for line in open(inputdir+"/"+f,"r"):
            if line[0]=="#":continue
            info=line.strip().split(" ")
            user=int(info[2][1:-1])
            if user not in us:continue
            social=info[0].split(":")
            idx=min(len(social)-1,1)
            fw.write("%d,%s\n"%(user,social[idx]))
        fw.close()
        solvecnt=solvecnt+1
        outputinfo("getSocialData[%s]"%(f),solvecnt,totalcnt,time.time()-starttime)
if __name__=="__main__":
    months=sys.argv[1:]
    for month in months:
        getInfomapData("network","community",month)
    #getSocialData("network","community","home")
