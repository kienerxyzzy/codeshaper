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
class Kule:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
IS_JAVASCRIPT=False#possibly supports JS, I mean they have similiar syntax

def readf(name):
    try:
        with open(name, "r") as f:
            c = f.read()
        print(f"{Kule.GREEN}File {name} read successfully{Kule.END}")
        return c
    except Exception as e:
        print(f"{Kule.RED}Error: Cannot read file {name}")
        print(f"Reason:{repr(e)}{Kule.END}")


code = readf("code.txt")
shape = readf("shape.txt")
commands = []
output=""
# (0,x): place x spaces
# (1,x): place x chars
# (2):newline
sz = 0
p = True
for char in shape:
    q = char == "." or char == " "
    if char == "\n":
        commands.append((0 if p else 1, sz))
        commands.append((2,))
        sz = 0
    elif p == q:
        sz += 1
    else:
        commands.append((0 if p else 1, sz))
        sz = 1
        p = q
data=handle(code)
ptr=0
sptr=-1
buf=""
plus=False
word=["dummy","dummy"]
def debug(*args,**kwargs):
    print(*args,**kwargs)
for c in commands:
    if c[0]==2:
        output+="\n"
        debug("CR",end=" ")
    elif c[0]==0:
        output+=" "*c[1]
        debug("BLANK",c[1],end=" ")
    else:
        
        debug("PUTS",c[1])
        buf=""
        while True:
            if ptr>=len(data):break
            debug("DEBUG",buf,c[1],data[ptr])
            if sptr==-1:
                #non-string word
                word=data[ptr]
                ptr+=1
                #debug("NEXT")
                debug("TOKEN",word)
                if word[0]!="string":
                    #we must fit the whole word in, otherwise we can stop here
                    if(len(buf)+len(word[1])>c[1]):
                        debug("NOFIT")
                        ptr-=1
                        break
                    buf+=word[1]
                elif 2+len(word[1])+len(buf)<=c[1]:
                    debug("WHOLE FIT")
                    #can fit whole string in here
                    buf+='"'+word[1]+'"'
                else:
                    #How many chars can one fit here?
                    chars=c[1]-len(buf)-2
                    if(chars<=1):
                        print("NARROW ERROR")
                        ptr-=1
                        break
                    debug("CAN FIT",chars)
                    buf+='"'
                    buf+=word[1][:chars]
                    buf+='"'
                    sptr=chars
                    plus=True
                #debug("DONE")
            elif plus:
                plus=False
                if(IS_JAVASCRIPT):continue
                if(1+len(buf)>c[1]):
                    break
                buf+="+"
                
            elif(2+len(word[1][sptr:])+len(buf)<=c[1]):
                #can fit whole string in here
                buf+='"'+word[1][sptr:]+'"'
                sptr=-1
                debug("SWHOLE FIT")
            else:
                #How many chars can one fit here?
                chars=c[1]-len(buf)-2
                if(chars<=1):
                    break
                debug("SCAN FIT",chars)
                buf+='"'
                buf+=word[1][sptr:sptr+chars]
                buf+='"'
                sptr+=chars
                plus=True
            
        diff=c[1]-len(buf)
        if diff>=4:
            buf+="/*"
            buf+="a"*(diff-4)
            buf+="*/"
        else:
            buf+=" "*diff
        output+=buf
        buf=""
try:
    with open("output.txt","w") as f:
        f.write(output)
    print(f"{Kule.GREEN}File output.txt written to successfully{Kule.END}")
except FileExistsError:
    print(f"{Kule.RED}Error: File output.txt already exists")
    print(f"To avoid loss of data we have prevented Python from overwriting what was there.")

except Exception as e:
    print(f"{Kule.RED}Error: Cannot write to file output.txt")
    print(f"Reason:{repr(e)}{Kule.END}")
