#include<cstdio>
#include<cstring>
#include<algorithm>
#include<vector>
using namespace std;
const double inf = 1e100;
const int maxn = 100000;
const int maxD = 2;
struct point {
    int id;
    double x[maxD];
    point() {}
    point(const double _x[],int _id){
        for(int i=0;i<2;i++){
            x[i]=_x[i];
        }
        id=_id;
    }
    void read() {
        scanf("%lf,%lf,%d",&x[0],&x[1],&id);
    }
};
vector<point> a;
point t[maxn];
int divX[maxn];
int n,now,K;
bool cmp(const point &a, const point &b) {
    return a.x[now] < b.x[now];
}
void buildTree(int left, int right, point a[]) {
    if (left >= right) return;
    int mid = (left + right) >> 1;
    double minx[maxD],maxx[maxD];
    for (int i=0; i<2; ++i) {
        minx[i]=inf;
        maxx[i]=-inf;
    }
    for (int i = left; i < right; i++) {
        for (int j=0; j<2; ++j) {
            minx[j]=min(minx[j],a[i].x[j]);
            maxx[j]=max(maxx[j],a[i].x[j]);
        }
    }
    now=0;
    for (int i=1; i<2; ++i){
        if (maxx[i]-minx[i]>maxx[now]-minx[now]) now=i;
    }
    divX[mid]=now;
    nth_element(a + left, a + mid, a + right, cmp);
    for(int i=0;i<2;i++)t[mid].x[i]=a[mid].x[i];
    t[mid].id=a[mid].id;
    if (left + 1 == right) return;
    buildTree(left, mid, a);
    buildTree(mid + 1, right, a);
}
double closestDist;
point closestNode;
void update(double d,point pt) {
    if(closestDist>d){
        closestDist=d;
        closestNode=pt;
    }
}
void findD(int left, int right,const point& p) {
    if (left >= right) return;
    int mid = (left + right) >> 1;
    double dx[maxD];
    double d=0;
    for (int i=0; i<2; ++i) {
        dx[i]=p.x[i]-t[mid].x[i];
        d+=dx[i]*dx[i];
    }
    update(d,t[mid]);
    if (left + 1 == right) return;
    double delta = dx[divX[mid]];
    double delta2 = delta*delta;
    int l1=left,r1=mid;
    int l2=mid+1,r2=right;
    if (delta>0) {
        swap(l1,l2);
        swap(r1,r2);
    }
    findD(l1, r1, p);
    if (delta2 < closestDist) findD(l2, r2, p);
}
void findNearestNeighbour(int n, const point& p) {
    closestDist=inf;
    findD(0, n, p);
}
void print(FILE* fp,char bid[]) {
    fprintf(fp,"%s,%d\n",bid,closestNode.id);
}
int main() {
    FILE *pointinfo=fopen("data/PointInfo.csv","r");
    FILE *baseinfo=fopen("data/BaseInfo.txt","r");
    FILE *bpmap=fopen("data/BasePointMap.txt","w");
    double x[2];
    int id,n=0;
    a.clear();
    while (fscanf(pointinfo,"%lf,%lf,%d",&x[0],&x[1],&id)!=-1) {
        a.push_back(point(x,id));
        n++;
    }
    vector<point> b(a);
    buildTree(0,n,&b[0]);
    char s[100];
    while(fscanf(baseinfo,"%s",s)!=-1){
        int idx=0;
        while(s[idx]!=',')idx++;
        sscanf(s+idx+1,"%lf,%lf",x,x+1);
        s[idx]='\0';
        findNearestNeighbour(n,point(x,-1));
        print(bpmap,s);
    }
    return 0;
}
