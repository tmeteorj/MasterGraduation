import time
import random
import os
import sys
import psutil
def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
def outputinfow(info):
    print("[%s] %s\n"%(gettime(),info))
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
def getMaxLabel(labs,maxv):
    opt=[]
    for x in labs:
        if labs[x]==maxv:
            opt.append(x)
    return random.choice(opt)
def getWeight(now,to):
    global edge,degree,cntedge
    return edge[now][to]/degree[now]
def iteration():
    global nodelabel,perm,edge
    for now in perm:
        labs=dict()
        maxv=-1
        for to in edge[now]:
            label=random.choice(nodelabel[to])
            weight=getWeight(now,to)
            if label in labs:labs[label]=labs[label]+weight
            else:labs[label]=weight
            maxv=max(maxv,labs[label])
        label=getMaxLabel(labs,maxv)
        nodelabel[now].append(label)
def initSLPA(filePath,widx):
    outputinfow("Start initSLPA: "+filePath)
    #month,ua,ub  cntcall,cntmess
    global nodelabel,edge,degree,cntedge,perm
    nodelabel=dict()
    edge=dict()
    degree=dict()
    cntedge=dict()
    perm=list()
    for line in open(filePath,"r"):
        info=line.strip().split("\t")
        us=[int(t) for t in info[0].strip().split(",")]
        cs=[int(t) for t in info[1].strip().split(",")]
        for u in us[1:]:
            if u not in degree:
                degree[u]=0
                cntedge[u]=0
                edge[u]=dict()
                nodelabel[u]=list()
                nodelabel[u].append(u)
                perm.append(u)
        edge[us[1]][us[2]]=cs[widx]
        degree[us[1]]+=cs[widx]
        cntedge[us[1]]+=1
        edge[us[2]][us[1]]=cs[widx]
        degree[us[2]]+=cs[widx]
        cntedge[us[2]]+=1
    outputinfow("End initSLPA: "+filePath)
def getMaxMark(li,thrscnt):
    cnt=dict()
    maxv=-1
    for x in li:
        if x in cnt:cnt[x]=cnt[x]+1
        else:cnt[x]=1
        maxv=max(maxv,cnt[x])
    ans=[]
    if maxv>=thrscnt:
        for x in cnt:
            if cnt[x]>=thrscnt:ans.append(x)
    else:
        for x in cnt:
            if cnt[x]==maxv:ans.append(x)
    return ans
def SLPA(filePath,itertimes,thrs,outputpath,widx):
    global perm,nodelabel
    initSLPA(filePath,widx)
    starttime=time.time()
    for it in range(itertimes):
        random.shuffle(perm)
        iteration()
        outputinfo("SLPA[%s]"%(filePath),it,itertimes,time.time()-starttime)
        if psutil.virtual_memory().percent>98:
            print("out of memory!!!!!!!!!!!!")
            sys.exit()
    thrscnt=int(itertimes*thrs/100)
    fw=open(outputpath,"w")
    comid=dict()
    idx=1
    for now in nodelabel:
        social=getMaxMark(nodelabel[now],thrscnt)
        fw.write(str(now))
        for x in social:
	        if(x not in comid):
		        comid[x]=idx
		        idx+=1
	        fw.write(","+str(comid[x]))
        fw.write("\n")
    fw.close()
def chooseOneFile(inputpath,outputpath,homepath):
    com=dict()
    cnt=0
    ucom=dict()
    for line in open(inputpath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        li=list()
        for x in inf[1:]:
            if x not in com:
                cnt=cnt+1
                com[x]=cnt
            li.append(com[x])
        ucom[info[0]]=random.choice(li)
    for line in open(homepath,"r"):
        info=[int(t) for t in line.strip().split(",")]
        if info[0] not in ucom:
            cnt=cnt+1
            ucom[info[0]]=cnt
    fw=open(outputpath,"w")
    for x in sorted(ucom.items(),key=lambda arg:arg[0]):
        fw.write("%d,%d\n"%(x[0],x[1]))
    fw.close()
def chooseOneDir(inputdir,outputdir):
    files=os.listdir(inputdir)
    solvecnt=0
    totalcnt=len(files)
    starttime=time.time()
    for f in files:
        chooseOneFile(inputdir+"/"+f,outputdir+"/"+f)
        solvecnt=solvecnt+1
        outputinfo("chooseOneFile[%s]"%(f),solvecnt,totalcnt,time.time()-starttime)
if __name__=="__main__":
    months=sys.argv[1:] 
#    for month in months:
#        SLPA("network/net"+month+".txt",100,100,"community/node"+month+".txt")
    chooseOneDir("community","communitySingle")
