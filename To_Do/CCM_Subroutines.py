#TDLF.py
#ADD -N CH 1,2 ACHIEVE -D 22/09/23 -C BIOL3611 -T READING

import numpy as np
import pandas as pd
import asyncio
import datetime as dt

def paramSplit(txt):
        ar = txt.split("-")
        params = []
        vals = []
        for i in ar:
            p = 0
            if len(i) <= 0:
                ar.pop(p)
                p = p-1
            p = p+1
        for i in range(len(ar)):
            br = ar[i].split(" ")
            if len(br[len(br)-1]) <= 0:
                br.pop()
            params.append(br[0])
            br.pop(0)
            apdstr = ""
            for i in br:
                #print(len(i))
                if (len(i) > 0):
                    if len(apdstr) == 0:
                        apdstr = apdstr + i
                    else:   
                        apdstr = apdstr + " " + i
           #print("apdstr: " +apdstr)
            if apdstr != "":
                vals.append(apdstr)
        params.pop(0)
        zipped = {params[i]: vals[i] for i in range(len(params))}
        return zipped
