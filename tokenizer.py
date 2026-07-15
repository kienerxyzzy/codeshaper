# Project Codeshaper
# Chapter I, the Tokeni(s/z)er
# Formatted with Black Formatter.
import tomllib

symbols = (
    list("+-*/%><!&|^~=.,?:;[](){}")
    + "== != >= <= && || >> << += -= *= /= %= &= |= ^= <<= >>= ++ -- -> ::".split()
)
symmers = "".join(list(set("".join(symbols))))
obfuscate="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
with open("config.toml", "rb") as f:
    cfg = tomllib.load(f)
OBFUSCATE = cfg["main"]["obfuscate"]
with open(cfg["files"]["reserved"]) as f:
    unsafe=(f.read().split("\n"))
DEFINES=cfg["defines"]
print(DEFINES,"\n".join(sorted(unsafe)))
def handle(code):
    cf = []
    mode = ""
    buf = ""
    op = 0
    od = {}
    for i in range(len(code)):
        c = code[i]
        if mode not in ["string", "char"] and c == "#":
            raise Warning("We do not support compiler directives.")
        if mode == "string":
            if c == '"':
                if code[i - 1] == "\\":
                    continue
                cf.append((mode, buf))
                mode = ""
                buf = ""
            else:
                buf += c
        elif mode == "char":
            cf.append(("number", str(ord(c))))
            mode = "char-wait"
        elif mode == "char-wait":
            mode = ""
        elif mode == "word":
            if c == "/":
                cf.append((mode, buf))
                if code[i + 1] == "*":
                    mode = "mlc"
                elif code[i + 1] == "/":
                    mode = "slc"
                else:
                    mode = "symbol"
                    buf = c
            elif c in symmers:
                cf.append((mode, buf))
                mode = "symbol"
                buf = c
            elif c in " \n\t":
                cf.append((mode, buf))
                mode = ""
                buf = ""
            elif c == '"':
                cf.append((mode, buf))
                mode = "string"
                buf = ""
            elif c == "'":
                cf.append((mode, buf))
                mode = "char"
                buf = ""
            else:
                buf += c
        elif mode == "number":
            if c in ".0123456789xABCDEF":
                buf += c
            elif c == "/":
                if code[i + 1] == "*":
                    mode = "mlc"
                elif code[i + 1] == "/":
                    mode = "slc"
            elif c in symmers:
                cf.append((mode, buf))
                mode = "symbol"
                buf = c
            elif c in " \n\t":
                cf.append((mode, buf))
                mode = ""
                buf = ""
            elif c == '"':
                cf.append((mode, buf))
                mode = "string"
                buf = ""
            elif c == "'":
                cf.append((mode, buf))
                mode = "char"
                buf = ""
            else:
                cf.append((mode, buf))
                mode = "word"
                buf = c

        elif mode == "symbol":
            if c == "/" and code[i + 1] in "*/":
                if code[i + 1] == "*":
                    mode = "mlc"
                elif code[i + 1] == "/":
                    mode = "slc"
            elif c in " \n\t":
                cf.append((mode, buf))
                mode = ""
                buf = ""
            elif c == '"':
                cf.append((mode, buf))
                mode = "string"
                buf = ""
            elif c == "'":
                cf.append((mode, buf))
                mode = "char"
                buf = ""
            elif buf + c not in symbols:
                cf.append((mode, buf))
                if c in symmers:
                    mode = "symbol"
                    buf = c
                elif c in "0123456789":
                    mode = "number"
                    buf = c
                else:
                    mode = "word"
                    buf = c
            else:
                buf += c
        elif mode == "":
            if c == "/" and code[i + 1] in "*/":
                if code[i + 1] == "*":
                    mode = "mlc"
                elif code[i + 1] == "/":
                    mode = "slc"
            elif c in " \n\t":
                mode = ""
                buf = ""
            elif c in symmers:
                mode = "symbol"
                buf = c
            elif c in "0123456789":
                mode = "number"
                buf = c
            elif c == '"':
                cf.append((mode, buf))
                mode = "string"
                buf = ""
            elif c == "'":
                cf.append((mode, buf))
                mode = "char"
                buf = ""
            else:
                mode = "word"
                buf = c
        elif mode == "mlc":
            if c == "/" and code[i - 1] == "*":
                mode = ""
                buf = ""
        elif mode == "slc":
            if c == "\n":
                mode = ""
                buf = ""
    defs=dict()
    for i in range(len(cf)):
        u = cf[i][0]
        t = cf[i][1]
        if u != "word":
            pass
        elif t == "true":
            cf[i] = ("number", "1")
        elif t == "false":
            cf[i] = ("number", "0")
        elif t in unsafe:pass
        elif OBFUSCATE:
            if t not in od:
                od[t] = obfuscate[op]
                print(t, "->", od[t])
                op += 1
            #print(t,"map to",od[t])
            if t in DEFINES:
                defs[od[t]]=DEFINES[t]
            cf[i] = (u, od[t])
        else:
            cf[i] = (u, t)
    cf2 = []
    for t in cf:
        if t[1] == "":
            continue
        if t[0] == "symbol":
            cf2.append(t)
        else:
            if len(cf2) > 0 and cf2[-1][0] in "word":  # split words
                cf2.append(("joiner", " "))
            cf2.append(t)
    return (cf2,defs)
