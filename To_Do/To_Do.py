import os
import numpy as np
import pandas as pd
import asyncio
import datetime as dt
import pyarrow
from CCM_Subroutines import *


import warnings
warnings.filterwarnings("ignore")

def initializer():
    os.system("cls")
    print()
    print("INITIALIZING...")
    #print()
    global tasks
    global taskCols
    taskCols = [ "DATE", "TYPE", "NAME", "CLASS"]
    try:
        tasks = pd.read_parquet(r'To_Do\ToDo_List.parquet')
        tasks = tasks[tasks.columns.intersection(taskCols)]
    except Exception as e:
        tasks = pd.DataFrame(columns = taskCols)
    tasks["DATE"] = pd.to_datetime(tasks["DATE"], dayfirst=True, format="%d/%m/%y", errors = "raise")
    tasks["DATE"] = tasks["DATE"].dt.strftime("%d/%m/%y")
    print("DATAFRAME CONSTRUCTED")
    print()
    global functs
    functs = {
         add : "ADD",
         complete : "COMPLETE",
         getInfo : "INFO",
         #long : "LONG",
         exit : "EXIT"
    }
    print("WELCOME, RED")

def exit(txt = ""):
    global running
    running = False

"""def long():
    pass"""

def printList():
    os.system("cls")
    print()
    today = dt.date.today()
    tasks["DATE"] = pd.to_datetime(tasks["DATE"]).dt.date
    a = tasks.mask(tasks["DATE"] < today).dropna()
    b = tasks.mask(tasks["DATE"] >= today).dropna()
    a["DATE"] = pd.to_datetime(a["DATE"], dayfirst=True, format="%d/%m/%y").dt.strftime("%d/%m/%y")
    b["DATE"] = pd.to_datetime(b["DATE"], dayfirst= True, format="%d/%m/%y").dt.strftime("%d/%m/%y")
    print("OVERDUE ASSIGNMENTS:")
    if len(b.index) > 0:
        a.index += len(b.index)-1
    else:
        print("    NO OVERDUE ASSIGNMENTS")
    a["INDEX"] = a.index
    for i in range(len(b.index)):
        print(i, ". ", b.iloc(axis = 0)[i]["DATE"], " ", b.iloc(axis = 0)[i]["CLASS"], " ", b.iloc(axis = 0)[i]["TYPE"], ": ", b.iloc(axis = 0)[i]["NAME"], sep = "")
    print()
    print("UPCOMING ASSIGNMENTS:")
    if len(a.index) > 0:
        for i in range(len(a.index)):
            print(a.iloc(axis=0)[i]["INDEX"], ". ", a.iloc(axis = 0)[i]["DATE"], " ", a.iloc(axis = 0)[i]["CLASS"], " ", a.iloc(axis = 0)[i]["TYPE"], ": ", a.iloc(axis = 0)[i]["NAME"], sep = "")
    else:
        print("    NO UPCOMING ASSIGNMENTS")
    print()
    print()


    

def complete(args):
    tasks.drop(int(args["I"]), inplace = True)


def add(args):
    aName = args["N"]
    Date = args["D"]
    aDate = pd.to_datetime(Date, dayfirst=True, format = "%d/%m/%y").strftime("%d/%m/%y")
    aType = args["T"]
    aClass = args["C"]
    apnd = [aDate, aType, aName, aClass]
    tasks.loc[len(tasks.index)] = apnd 
    print(tasks)
    


def getInfo(args):
    ind = args["I"]
    info = args["F"]
    print(tasks.iloc(axis = 0)[ind][info])


def main():
    global running
    running = True
    initializer()
    while (running):
            tasks["DATE"] = pd.to_datetime(tasks["DATE"], format="%d/%m/%y").dt.strftime("%d/%m/%y")
            tasks.sort_values(by="DATE", ignore_index=True, inplace=True)
            printList()
            uIn = input(">>")
            uIn = uIn.upper()
            if "-" in uIn:
                hold = uIn.split("-")
                command = hold[0]
                command = command[:len(command)-1]
            else:
                command = uIn
            try:
                call = [k for k, v in functs.items() if v == command][0]
                args = paramSplit(uIn)
                call(args)
            except Exception as e:
                print("ERROR: UNRECOGNIZED COMMAND")
    tasks.to_parquet(path=r"To_Do\ToDo_List.parquet")

main()

os.system("cls")

try:
    with("LANDING.PY") as f:
        exec(f.read())
except Exception as e:
    pass
