import os
import numpy as np
import pandas as pd
import asyncio
import datetime as dt
import pyarrow
from CCM_Subroutines import *
import subprocess
from rich.console import Console
from rich.traceback import install
from rich.table import Table

install()
console = Console()

"""import warnings
warnings.filterwarnings("ignore")"""

def initializer():
    os.system("cls")
    print()
    print("INITIALIZING...")

    global today
    global tasks
    global taskCols

    taskCols = [ "DATE", "TYPE", "NAME", "CLASS", "CODES"]
    today = dt.date.today()

    try:
        tasks = pd.read_parquet(r'CCM\ToDo_List.parquet')
        tasks = tasks[tasks.columns.intersection(taskCols)]
        print(tasks)
    except Exception as e:
        tasks = pd.DataFrame(columns = taskCols)
    tasks["DATE"] = pd.to_datetime(tasks["DATE"], dayfirst=True, format="%d/%m/%y", errors = "raise").dt.date
    #tasks["DATE"] = tasks["DATE"].strftime("%d/%m/%y")
    tasks = tasks.reindex(columns=taskCols, fill_value="")

    for i in tasks.index:
        print(i)
        #print(type())
        if (tasks.iloc[i]["DATE"] > today) and ("!" not in tasks.iloc[i]["CODES"]):
            if len(tasks.iloc[i]["CODES"]) == 0:
                tasks.iloc[i]["CODES"] = tasks.iloc[i]["CODES"] + "!"
            else:
                tasks.iloc[i]["CODES"] = tasks.iloc[i]["CODES"] + ", !"
                
        

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
    subprocess.run(["Python", "To_Do\LANDING.py"])

"""def long():
    pass"""

def printList():
    #os.system("cls")
    print()
    global today
    today = dt.date.today()
    tasks["DATE"] = pd.to_datetime(tasks["DATE"], dayfirst= True, format = "%d/%m/%y").dt.date
    tasks.sort_values(by="DATE", ignore_index=True, inplace=True)

    table = Table(title="TASKS")
    columns = ["I", "CODES", "TYPE", "NAME", "CLASS", "DATE"]
    style = "green"
    for i in range(len(columns)):
        table.add_column(f"{columns[i]}", style = style)
    for i in range(len(tasks.index)):
        date = tasks.iloc(axis=0)[i]["DATE"]
        if len(str(date.day)) < 2:
            prdate = "0" + str(date.day) + "/"
        else:
            prdate = str(date.day) + "/"
        if len(str(date.month)) < 2:
            prdate = prdate + "0" + str(date.month)
        else:
            prdate = prdate + str(date.month)
        if len(tasks.iloc(axis=0)[i]["CODES"]) > 0:
            table.add_row(str(i), tasks.iloc(axis=0)[i]["CODES"], tasks.iloc(axis=0)[i]["TYPE"], tasks.iloc(axis=0)[i]["NAME"], tasks.iloc(axis=0)[i]["CLASS"], prdate)
        else:
            table.add_row(str(i), "X", tasks.iloc(axis=0)[i]["TYPE"], tasks.iloc(axis=0)[i]["NAME"], tasks.iloc(axis=0)[i]["CLASS"], prdate)            
    console.print(table)
    


def printConsole():
    global error
    os.system("cls")
    try:
        print(error)
    except Exception as e:
        console.print_exception()
    print()
    today = dt.date.today()
    tasks["DATE"] = pd.to_datetime(tasks["DATE"]).dt.date
    a = tasks.mask(tasks["DATE"] < today).dropna()
    b = tasks.mask(tasks["DATE"] >= today).dropna()
    a["DATE"] = pd.to_datetime(a["DATE"], dayfirst=True, format="%d/%m/%y").dt.strftime("%d/%m/%y")
    b["DATE"] = pd.to_datetime(b["DATE"], dayfirst= True, format="%d/%m/%y").dt.strftime("%d/%m/%y")
    

def complete(args):
    tasks.drop(int(args["I"]), inplace = True)


def add(args):
    global aName, aType, aClass, aDate, aCode
    global error
    try:
        aName = args["N"]
        Date = args["D"]
        aDate = pd.to_datetime(Date, dayfirst=True, format = "%d/%m/%y").strftime("%d/%m/%y")
        aType = args["T"]
        aClass = args["C"]
        aCode = args["A"]
    except Exception as e:
        console.print_exception()
        error = "ERROR: ADDITION FAILED"


    apnd = [aDate, aType, aName, aClass, aCode]
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
            if command in functs.items():
                call = [k for k, v in functs.items() if v == command][0]
                args = paramSplit(uIn)
                call(args)
            else:
                print("ERROR: UNRECOGNIZED COMMAND")
    tasks.to_parquet(path=r"CCM\ToDo_List.parquet")

main()

os.system("cls")

try:
    with("LANDING.PY") as f:
        exec(f.read())
except Exception as e:
    console.print_exception()
    pass
