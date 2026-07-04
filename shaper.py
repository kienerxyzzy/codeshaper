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
using namespace std;
//Implements most arith instructions
//using only NAND, SHL, SHR and equality tests.
const int VS_LEN=16;
const int VS_RADIX=2;

const char charset[17]="0123456789abcdef";
string visualize(nanpa N){
    string out;
    nanpa T=N;
    for(int i=0;i<VS_LEN;i++){
        out=charset[T%VS_RADIX]+out;
        T/=VS_RADIX;
    }
    return out;
}
void debug(string label, nanpa N){
    cout<<label<<": "<<visualize(N)<<" (Decimal "<<(int)N<<")"<<endl;
    //does display with sign
}
const nanpa nxor=UINT_MAX;
//a number with all bits set to 1
int nandc,shlc,shrc,eqc;
nanpa xnand(nanpa x, nanpa y){
    nanpa r=(x&y)^nxor;
    //cout<<visualize(x)<<" NAND "<<visualize(y)<<" = "<<visualize(r)<<endl;
    nandc++;
    return r;
}
nanpa xshl(nanpa x){
    nanpa r=x<<1;
    //cout<<visualize(x)<<" SHL = "<<visualize(r)<<endl;
    shlc++;
    return r;
}
nanpa xshr(nanpa x){
    nanpa r=x>>1;
    //cout<<visualize(x)<<" SHR = "<<visualize(r)<<endl;
    shrc++;
    return r;
}
nanpa xeq(nanpa x, nanpa y){
    bool r=(x==y);
    //cout<<visualize(x)<<" == "<<visualize(y)<<" -> "<<r<<endl;
    eqc++;
    return r;
}
//now that the prereqs are out of my way, functions begin here
nanpa xadd(nanpa x,nanpa y){
    if(xeq(y,0)){return x;}
    nanpa mand,mxor;
    mand=xnand(x,y);
    mxor=xnand(xnand(x,mand),xnand(y,mand));
    mand=xshl(xnand(mand,mand));
    return xadd(mxor,mand);
}
nanpa x1cmp(nanpa x){return xnand(x,x);}
nanpa x2cmp(nanpa x){return x1cmp(xadd(x,nxor));}
nanpa xsub(nanpa x,nanpa y){
    return xadd(x,x2cmp(y));
}
nanpa xand(nanpa x,nanpa y){
    return x1cmp(xnand(x,y));
}
nanpa xmul(nanpa x,nanpa y){
    if(xeq(y,0)){return 0;}
    if(xeq(y,1)){return x;}
    nanpa p=xshl(xmul(x,xshr(y)));
    if(xeq(xand(y,1),1)){
        return xadd(p,x);
    }else{
        return p;
    }
}
nanpa m,n;
int main(){
    m=36;
    n=67;
    debug("A",m);
    debug("B",n);
    debug("A*B",xmul(m,n));
    cout<<"====MACHINE STATISTICS===="<<endl;
    cout<<"NAND was triggered "<<nandc<<" time(s)"<<endl;
    cout<<"SHL was triggered "<<shlc<<" time(s)"<<endl;
    cout<<"SHR was triggered "<<shrc<<" time(s)"<<endl;
    cout<<"TEQ was triggered "<<eqc<<" time(s)"<<endl;
}

"""
l = [i[1] for i in handle(code)]
s = ""
for c in l:
    if len(c) + len(s) > 40:
        print(s)
        s = c
    else:
        s += c
print(s)  # this will print out C++ code that actually compiles and runs properly
# trust me, I've compiled it
