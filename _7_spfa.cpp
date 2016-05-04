/*************************************************************************
	> File Name: _7_spfa.cpp
	> Author:
	> Mail:
	> Created Time: 2016年04月29日 星期五 14时48分01秒
 ************************************************************************/

#include<cstdio>
#include<memory.h>
#include<iostream>
#include<ctime>
using namespace std;
const int N=59203,M=N*4;
struct Edge{
    int to,next;
    double cost;
}edge[M];
int head[N+1],pre[N+1],nc;
double dist[N+1];
bool in[N+1];
int L[N];
void add(int a,int b,double c){
    edge[nc].to=b;
    edge[nc].cost=c;
    edge[nc].next=head[a];
    head[a]=nc++;
}
void spfa(int src,FILE *f){
    for(int i=0;i<N;i++){
        dist[i]=1e100;
        in[i]=false;
    }
    int front=0,rear=0;
    L[rear++]=src;
    dist[src]=0;
    in[src]=true;
    pre[src]=src;
    while(front!=rear){
        int now=L[front++];
        in[now]=false;
        if(front==N)front=0;
        for(int i=head[now];i!=-1;i=edge[i].next){
            int to=edge[i].to;
            double cost=edge[i].cost;
            if(dist[to]>dist[now]+cost){
                dist[to]=dist[now]+cost;
                pre[to]=now;
                if(!in[to]){
                    in[to]=true;
                    L[rear++]=to;
                    if(rear==N)rear=0;
                }
            }
        }
    }
    for(int i=0;i<N;i++){
        fprintf(f,"%d:%f%c",pre[i],dist[i],i==N-1?'\n':' ');
    }
}
int main(){
    freopen("RoadEdge.csv","r",stdin);
    FILE *f=fopen("DistMat.csv","w+");
    memset(head,-1,sizeof(head));
    nc=0;
    int a,b;
    double c;
    while(scanf("%d%d%lf",&a,&b,&c)!=EOF){
        add(a,b,c);
        add(b,a,c);
    }
    long start=clock();
    for(int i=0;i<N;i++){
        spfa(i,f);
        long res=(long)((clock()-start)/1000.0/(i+1.0)*(N-i-1.0));
        int h=res/3600,m=res%3600/60,s=res%60;
        printf("spfa[%d]: remain:%02d:%02d:%02d\n",i,h,m,s);
    }
    fclose(f);
    return 0;
}
