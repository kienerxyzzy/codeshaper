# Project Codeshaper
# Chapter II, the Shaper

# So you know how on IOCCC people often write their code in a way that makes it resemble an image?
# Well, I want to do that, but without putting too much work in it. So I'm creating an engine to do that for me.
from tokenizer import handle

# handle(code):
# code is a C++ script
# Returns a list of tuples (a,b). a can be "word","number","symbol","string" or "joiner".
# The function also obfuscates variables and functions (though smart enough to not touch the reserved stuff)
# The tokens are also engineered in such a way that one can concatenate their bodies and form a mess of obfuscated code.

# By the way, "joiner" tokens consist of a single space and only appears in the boundary
# between a word and another word or a number.
# The only real issue is that it doesn't support compiler directives.
code = """
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
l = [i[1] for i in handle(code)]
s = ""
for c in l:
    if len(c) + len(s) > 20:
        print(s)
        s = c
    else:
        s += c
print(s)  # this will print out C++ code that actually compiles and runs properly
# trust me, I've compiled it
