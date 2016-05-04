#!/usr/bin/env python
# coding=utf-8
import sys
import random
import gzip
def makeint2(minnum,maxnum):
    return minnum+makeint(maxnum-minnum)
def makeint(maxnum):
    return int(random.random()*maxnum)
def makeanrecord(year,month,day):
    t=random.choice([1,3,6,7,12,13])
    h=makeint(24)
    m=makeint(60)
    s=makeint(60)
    big=makeint(10000)
    small=makeint(10000)
    u1=makeint(1000)
    u2=makeint(1000)
    return "%d,%04d%02d%02d %02d:%02d:%02d,%d,%d,%d,%d,%d,%d\n"%(t,year,month,day,h,m,s,big,small,u1,u1,u2,u2)
def makeanday(year,month,day,fw,num):
    for i in range(num):
        fw.write(makeanrecord(year,month,day))
def makeanmonth(year,month,minv,maxv,fw):
    print("makeanmonth",year,month)
    if month in [1,3,5,7,8,10,12]:daycnt=31
    elif month!=2:daycnt=30
    else:daycnt=28+(1 if year%400==0 or (year%4==0 and year%100!=0) else 0)
    for day in range(1,daycnt+1):
        makeanday(year,month,day,fw,makeint2(minv,maxv))
def makeMat(path,n,m):
    fw=open(path,"w")
    for i in range(n):
        for j in range(m):
            fw.write(str(random.random()*1000))
            if j==m-1:fw.write("\n")
            else:fw.write(" ")
    fw.close()
def makeMats(dirpath,tot,n):
    fl=tot//n
    for i in range(fl):
        makeMat(dirpath+"/MatDist"+str(i)+".txt",n,tot)
    if tot%n!=0:
        n=tot-n*fl
        makeMat(dirpath+"/MatDist"+str(fl)+".txt",n,tot)
if __name__=="__main__":
    makeMats("Mat",106,10)
