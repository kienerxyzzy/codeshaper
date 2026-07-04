# Project Codeshaper
# Chapter I, the Tokeni(s/z)er
# Formatted with Black Formatter.
symbols = (
    list("+-*/%><!&|^~=.,?:;[](){}")
    + "== != >= <= && || >> << += -= *= /= %= &= |= ^= <<= >>= ++ -- -> ::".split()
)
symmers = "".join(list(set("".join(symbols))))
unsafe = "UINT_MAX const void string ifstream file ios is_open istreambuf_iterator char size push_back erase default binary switch case LLONG_MAX INT_MAX else bool long unsigned if main for endl while true std return namespace cin int continue break resize vector map set unordered_map unordered_set using cout false".split()
from random import shuffle

temp = list("abcdefghijklmnopqrstuvwxyz")
shuffle(temp)
obfuscate = temp
temp = list("ABCDEFGIHJKLMNOPQRSTUVWXYZ")
shuffle(temp)
obfuscate += temp


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
    for i in range(len(cf)):
        u = cf[i][0]
        t = cf[i][1]
        if u == "string":
            cf[i] = ("string", '"' + t + '"')
        if u != "word":
            continue
        if t == "true":
            cf[i] = ("number", "1")
        if t == "false":
            cf[i] = ("number", "0")
        if t in unsafe:
            continue
        if t not in od:
            od[t] = obfuscate[op]
            print(t, "->", od[t])
            op += 1
        cf[i] = (u, od[t])
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
    return cf2
