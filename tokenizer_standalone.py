from tokenizer import handle

src = """
using namespace std;
string compact_tokens="$";
vector<pair<int,string>> tokens;
int p,sp;
pair<int,string> temp;
char q=34;
const char S[]="CHXHCNVN ";
int m,em;
bool codes(int c,bool b=false){
    int cs=0;
    bool flag;
    flag=true;
    while(1){
        if(p>=tokens.size()){
            flag=false;
            break;
        }
        if(sp==-1){
            temp=tokens[p];
            if(temp.first!=2){
                if(temp.second.size()+cs>c){
                    break;
                }else{
                    p++;
                    cout<<temp.second;
                    cs+=temp.second.size();
                }
            }else if(2+temp.second.size()+cs<=c){
                cout<<q<<temp.second<<q;
                cs+=(2+temp.second.size());
                p++;
            }else{
                if(cs+2>c){break;}
                sp=0;
            }
        }else if((2+temp.second.size()-sp+cs)<=c){
            cout<<q;
            for(int i=sp;i<temp.second.size();i++){
                cout<<temp.second[i];
            }
            cout<<q;
            cs+=(2+temp.second.size()-sp);
            sp=-1;
            p++;
        }else{
            int tempc=c-cs-2;
            if(tempc<=1){break;}
            cs=c;
            cout<<q;
            for(int i=sp;i<sp+tempc;i++){
                cout<<temp.second[i];
            }
            sp+=tempc;
            cout<<q;
        }
    }
    if(c-cs>=4){
        cout<<"/*";
        for(int i=0;i<c-(cs+4);i++){
            cout<<S[i%9];
        }
        cout<<"*/";
    }else{
        for(int i=cs;i<c;i++){
            cout<<" ";
        }
    }
    if(b){cout<<endl;}
    return flag;
}
const int SubWidth=72;
void box(string S, int offset){
    codes(offset);
    cout<<"/*+";
    for(int i=0;i<S.size()+2;i++){
        cout<<"-";
    }
    cout<<"+*/";
    codes(SubWidth-S.size()-offset,1);
    codes(offset);
    cout<<"/*|";
    for(int i=0;i<S.size()+2;i++){
        cout<<" ";
    }
    cout<<"|*/";
    codes(SubWidth-S.size()-offset,1);
    codes(offset);
    cout<<"/*| "<<S<<" |*/";
    codes(SubWidth-S.size()-offset,1);
    codes(offset);
    cout<<"/*|";
    for(int i=0;i<S.size()+2;i++){
        cout<<" ";
    }
    cout<<"|*/";
    codes(SubWidth-S.size()-offset,1);
    codes(offset);
    cout<<"/*+";
    for(int i=0;i<S.size()+2;i++){
        cout<<"-";
    }
    cout<<"+*/";
    codes(SubWidth-S.size()-offset,1);
    codes(SubWidth+8,1);
}
vector<vector<char>> grid;
void line(int x0, int y0, int x1, int y1){
    //cout<<"("<<x0<<","<<y0<<")"<<"=>("<<x1<<","<<y1<<")"<<endl;
    int dx=abs(x1-x0);int dy=abs(y1-y0);
    int sx=(x0<x1) ? 1 : -1;
    int sy=(y0<y1)?1:-1;
    int e=dx-dy;
    while(1){
        grid[x0][y0]=1;
        if(x0==x1 && y0==y1){break;}
        int tmp=e<<1;
        if(tmp>-dy){e-=dy;x0+=sx;}
        if(tmp<dx){e+=dx;y0+=sy;}
    }
}
const double cn=0.628318530718;
int main(){
    cout<<(char)35<<"include <bits/stdc++.h>"<<endl;
    m=-1;
    temp.first=0;
    temp.second="";
    for(auto c : compact_tokens){
        if(c=='@'){em=1;}
        else if(c=='#'){em=2;}
        else if(c=='~'){em=0;}
        else{em=m;temp.second+=c;continue;}
        if(m!=-1){
            if(temp.first==2 && temp.second[0]=='$'){
                temp.second=compact_tokens;
            }
            tokens.push_back(temp);
        }
        m=em;
        temp.first=em;
        temp.second="";
    }
    sp=-1;
    p=0;
    grid.resize(192,vector<char>(72,0));
    for(int i=0;i<10;i++){
        double x0=(i&1?2:1)*sin(cn*i)+4;
        double y0=((i&1)+1)*cos(i*cn)+3;
        double x1=(i&1?1:2)*sin(cn*i+cn)+4;
        double y1=(2-(i&1))*cos(cn*(i+1))+3;
        line(round(24*x0),round(12*y0),round(24*x1),round(12*y1));
    }
    queue<pair<int,int>> flood;
    flood.push({96,36});
    while(!flood.empty()){
        int xt=flood.front().first;
        int yt=flood.front().second;
        flood.pop();
        if(grid[xt][yt]==1){continue;}
        grid[xt][yt]=1;
        flood.push({xt+1,yt});
        flood.push({xt,yt+1});
        flood.push({xt-1,yt});
        flood.push({xt,yt-1});
    }
    int b=0;
    for(int f=0;f<2;f++){
        cout<<(char)27<<"[91m"<<(char)27<<"[41m";
        for(int i=0;i<4;i++){codes(202,1);}
        cout<<(char)27<<(char)27<<"[101m";
        for(int i=0;i<72;i++){
            cout<<(char)27<<"[41m";
            codes(6);
            cout<<(char)27<<"[101m";
            for(int j=0;j<192;j++){
                if(grid[j][i]){
                    b++;
                }else{
                    if(b>0){
                        cout<<(char)27<<"[103m";
                        codes(b);
                        cout<<(char)27<<"[101m";
                    }
                    cout<<" ";
                    b=0;
                }
            }
            cout<<(char)27<<"[41m";
            codes(6);
            cout<<(char)27<<"[0m"<<endl<<(char)27<<"[91m";
        }

        cout<<(char)27<<"[41m";
        for(int i=0;i<4;i++){codes(202,1);}
        cout<<(char)27<<"[0m"<<endl;
    }
}

"""
d={}

S = ""
t = {
    "word": "~",
    "number": "~",
    "symbol": "~",
    "string": "#",
}
print(handle(src))
for i,j in handle(src)[0]:
    if i=="joiner":
        S+="@ "
    else:
        S+=(t[i]+j)
T=""
for i,j in enumerate(S):
    t=ord(j)
    T+=chr(t)
print(T)