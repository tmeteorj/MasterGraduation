import time
import random
import os
import psutil
def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
def outputinfo(info):
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
    outputinfo("Start initSLPA: "+filePath)
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
    outputinfo("End initSLPA: "+filePath)
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
def SLPA(filePath,itertimes,thrs,outputpath):
    global perm,nodelabel
    initSLPA(filePath)
    starttime=time.time()
    for it in range(itertimes):
        random.shuffle(perm)
        iteration()
        outputinfo("SLPA[%s]"%(filePath),it,itertimes,time.time()-starttime)
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
if __name__=="__main__":
    months=sys.argv[1:] 
    for month in months:
        SLPA("network/net"+month+".txt",100,100,"community/node"+month+".txt")
