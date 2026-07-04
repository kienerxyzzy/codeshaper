code="""
using namespace std;
/* The UM-32 is a 32-bit processor created by the fictional Cult of the Bound Variable introduced in ICFP 2006.
 * It's been 20 years, but I simply cannot let a processor-related problem slide.
 * Now, I already have a Python implementation of the thing, but it's unbearably slow.
 * So now I'm writing some C++ code to hopefully get it up to a good speed?
 * We'll see.
 * Update: I ran the SANDmark
*/
const uint allone=0xFFFFFFFF;
uint allot_ptr;
unordered_map<uint,vector<uint>> arrays;
bool running;
void init(){
    string program;
    while(1){
        string filename;
        cout<<"filename:";
        cin>>filename;
        ifstream file(filename,ios::binary);
        if(!file.is_open()){
            cout<<"error"<<endl;
            continue;
        }else{
            program=string((istreambuf_iterator<char>(file)),istreambuf_iterator<char>());
            break;
        }

    }
    arrays[0];
    uint temp;
    temp=0;
    for(int i=0;i<program.size();i+=4){
        temp=(unsigned char)program[i]<<24;
        temp|=(unsigned char)program[i+1]<<16;
        temp|=(unsigned char)program[i+2]<<8;
        temp|=(unsigned char)program[i+3];
        //if(i<400){cout<<temp<<" ";}
        arrays[0].push_back(temp);
    }
    cout<<"copying finished ("<<arrays[0].size()<<" platters)"<<endl;
    running=true;
}
string buffer="";
uint bufptr=1;
uint inp(){
    string temp;
    if(bufptr>buffer.size()){
        buffer="";
        bufptr=0;
        while(cin>>temp){
            buffer+=temp;
        }
    }
    uint retval;
    if(bufptr>=buffer.size()){
        retval=allone;
    }else{
        retval=buffer[bufptr];
    }
    bufptr++;
    return retval;
}
uint regs[8];
uint pc,op,a,b,c;
int main(){
    init();
    while(running){
        op=arrays[0][pc];
        a=(op>>6)&7;
        b=(op>>3)&7;
        c=op&7;
        //cout<<"running "<<op<<endl;
        switch(op>>28){
        case 0:
            if(regs[c]!=0){regs[a]=regs[b];}
            break;
        case 1:
            regs[a]=arrays[regs[b]][regs[c]];
            break;
        case 2:
            arrays[regs[a]][regs[b]]=regs[c];
            break;
        case 3:
            regs[a]=regs[b]+regs[c];
            break;
        case 4:
            regs[a]=regs[b]*regs[c];
            break;
        case 5:
            regs[a]=regs[b]/regs[c];
            break;
        case 6:
            regs[a]=~(regs[b]&regs[c]);
            break;
        case 7:
            running=false;
            break;
        case 8:
            allot_ptr++;
            arrays[allot_ptr];
            arrays[allot_ptr].resize(regs[c]);
            regs[b]=allot_ptr;
            break;
        case 9:
            arrays.erase(regs[c]);
            break;
        case 10:
            cout<<(char)(regs[c]);
            break;
        case 11:
            regs[c]=inp();
            break;
        case 12:
            if(regs[b]!=0){
                arrays[0]=arrays[regs[b]];
            }
            pc=regs[c]-1;
            break;
        case 13:
            regs[(op>>25)&7]=op&0x1FFFFFF;
            break;
        default:
            cout<<"invalid opcode";
            running=false;
            break;

        }
        pc++;
    }
    cout<<"program halted"<<endl;
}

"""
#Project Codeshaper
#Chapter I, the Tokeni(s/z)er
symbols=list("+-*/%><!&|^~=.,?:;[](){}")+"== != >= <= && || >> << += -= *= /= %= &= |= ^= <<= >>= ++ -- -> ::".split()
symmers="".join(list(set("".join(symbols))))
unsafe="const void string ifstream file ios is_open istreambuf_iterator char size push_back erase default binary switch case LLONG_MAX INT_MAX else bool long unsigned if main for endl while true std return namespace cin int continue break resize vector map set unordered_map unordered_set using cout false".split()
from random import shuffle
temp=list("abcdefghijklmnopqrstuvwxyz")
shuffle(temp)
obfuscate=temp
temp=list("ABCDEFGIHJKLMNOPQRSTUVWXYZ")
shuffle(temp)
obfuscate+=temp
def handle(code):
  cf=[]
  mode=""
  buf=""
  op=0
  od={}
  for i in range(len(code)):
    c=code[i]
    if mode not in ["string","char"] and c=="#":
      raise Warning("We do not support compiler directives.")
    if mode=="string":
      if c=='"':
        if code[i-1]=='\\':continue
        cf.append((mode,buf))
        mode=""
        buf=""
      else:
        buf+=c
    elif mode=="char":
      cf.append(("number",ord(c)))
      mode="char-wait"
    elif mode=="char-wait":
      mode=""
    elif mode=="word":
      if c=="/":
        cf.append((mode,buf))
        if code[i+1]=="*":
          mode="mlc"
        elif code[i+1]=="/":
          mode="slc"
        else:
          mode="symbol"
          buf=c
      elif c in symmers:
        cf.append((mode,buf))
        mode="symbol"
        buf=c
      elif c in "0123456789":
        cf.append((mode,buf))
        mode="number"
        buf=c
      elif c in " \n\t":
        cf.append((mode,buf))
        mode=""
        buf=""
      elif c=='"':
        cf.append((mode,buf))
        mode="string"
        buf=""
      elif c=="'":
        cf.append((mode,buf))
        mode="char"
        buf=""
      else:
        buf+=c
    elif mode=="number":
      if c in ".0123456789xABCDEF":
        buf+=c
      elif c=="/":
        if code[i+1]=="*":
          mode="mlc"
        elif code[i+1]=="/":
          mode="slc"
      elif c in symmers:
        cf.append((mode,buf))
        mode="symbol"
        buf=c
      elif c in " \n\t":
        cf.append((mode,buf))
        mode=""
        buf=""
      elif c=='"':
        cf.append((mode,buf))
        mode="string"
        buf=""
      elif c=="'":
        cf.append((mode,buf))
        mode="char"
        buf=""
      else:
        cf.append((mode,buf))
        mode="word"
        buf=c
      
    elif mode=="symbol":
      if c=="/" and code[i+1] in "*/":
        if code[i+1]=="*":
          mode="mlc"
        elif code[i+1]=="/":
          mode="slc"
      elif c in " \n\t":
        cf.append((mode,buf))
        mode=""
        buf=""
      elif c=='"':
        cf.append((mode,buf))
        mode="string"
        buf=""
      elif c=="'":
        cf.append((mode,buf))
        mode="char"
        buf=""
      elif buf+c not in symbols:
        cf.append((mode,buf))
        if c in symmers:
          mode="symbol"
          buf=c
        elif c in "0123456789":
          mode="number"
          buf=c
        else:
          mode="word"
          buf=c
      else:
        buf+=c
    elif mode=="":
      if c=="/" and code[i+1] in "*/":
        if code[i+1]=="*":
          mode="mlc"
        elif code[i+1]=="/":
          mode="slc"
      elif c in " \n\t":
        mode=""
        buf=""
      elif c in symmers:
        mode="symbol"
        buf=c
      elif c in "0123456789":
        mode="number"
        buf=c
      elif c=='"':
        cf.append((mode,buf))
        mode="string"
        buf=""
      elif c=="'":
        cf.append((mode,buf))
        mode="char"
        buf=""
      else:
        mode="word"
        buf=c
    elif mode=="mlc":
      if c=="/" and code[i-1]=="*":
        mode=""
        buf=""
    elif mode=="slc":
      if c=="\n":
        mode=""
        buf=""
  for i in range(len(cf)):
    u=cf[i][0]
    t=cf[i][1]
    if u=="string":
      cf[i]=("string",'"'+t+'"')
    if u!="word":continue
    if t=="true":
      cf[i]=(("number","1"))
    if t=="false":
      cf[i]=(("number","0"))
    if t in unsafe:continue
    if t not in od:
      od[t]=obfuscate[op]
      print(t,"->",od[t])
      op+=1
    cf[i]=(u,od[t])
  #Word Fusion: 2 words next to each other get fused as 1 token and joined with spaces
  cf2=[]
  for t in cf:
    if t[0]=="symbol":
      cf2.append(t)
    else:
      if len(cf2)>0 and cf2[-1][0] in "word":#same with numbers, return 0 should be seperated
        cf2[-1]=("word",cf2[-1][1]+" "+t[1])
      else:
        cf2.append(t)
  return cf2
    
    
