import os
import pandas as pd
import asyncio
import datetime as dt
from CCM_Subroutines import *
from rich.console import Console
from rich.traceback import install
from rich.table import Table
from config import *
from rich.prompt import Prompt
from rich.theme import Theme

file = os.path.basename(__file__)
user = os.getlogin()

import warnings
warnings.filterwarnings("ignore")


#install()

console = Console()


def initializer():
    os.system("cls")
    console.print("INITIALIZING...",style = theme, highlight=False),
    global tasks
    tasks = initTasks()
    
    global functs
    functs = {
         add : "ADD",
         complete : "RM",
         #getInfo : "INFO",
         long : "LONG",
         exit : "EXIT",
         landing : "HOME",
         short : "SHORT",
         l : "L"
    }
    global command
    command = "INIT"
    console.print("SUCCESS!", style = theme)
    console.print("WELCOME, RED", style = theme)

def short():
    pass

def l():
    long()

def long():
    print()

    global today
    today = dt.date.today()

    tasks["DATE"] = pd.to_datetime(tasks["DATE"], dayfirst= True, format = "%d/%m/%y").dt.date
    tasks.sort_values(by="DATE", ignore_index=True, inplace=True)

    table = Table(title="TASKS")
    columns = ["I", "CODES", "TYPE", "NAME", "CLASS", "DATE"]
    style = "green"

    for i in range(len(columns)):
        table.add_column(f"{columns[i]}", style = theme)
    for i in range(len(tasks.index)):
        date = tasks.iloc(axis=0)[i]["DATE"]
        if len(str(date.day)) < 2:
            prdate = "0" + str(date.day) + "/"
        else:
            prdate = str(date.day) + "/"
        if len(str(date.month)) < 2:
            prdate = prdate + "0" + str(date.month) + "/"
        else:
            prdate = prdate + str(date.month) + "/"
        prdate = prdate + str(date.year)
        if len(tasks.iloc(axis=0)[i]["CODES"]) > 0:
            table.add_row(str(i), tasks.iloc(axis=0)[i]["CODES"], tasks.iloc(axis=0)[i]["TYPE"], tasks.iloc(axis=0)[i]["NAME"], tasks.iloc(axis=0)[i]["CLASS"], prdate)
        else:
            table.add_row(str(i), "X", tasks.iloc(axis=0)[i]["TYPE"], tasks.iloc(axis=0)[i]["NAME"], tasks.iloc(axis=0)[i]["CLASS"], prdate) 

    console.print(table)
    print()

def printList():
    global command
    """if command != "INIT":
        os.system("cls")
        print()"""

    global today
        
    today = dt.date.today()
    tasks["DATE"] = pd.to_datetime(tasks["DATE"], dayfirst= True, format = "%d/%m/%y").dt.date
    tasks.sort_values(by="DATE", ignore_index=True, inplace=True)
    prtasks = tasks.mask(tasks["DATE"] > (today+ dt.timedelta(days = List_Time)))
    prtasks["DATE"] = pd.to_datetime(tasks["DATE"], dayfirst= True, format = "%d/%m/%y").dt.date
    prtasks.sort_values(by="DATE", ignore_index=True, inplace=True)
    prtasks.dropna(inplace=True)
    for i in prtasks.columns:
        if i != "DATE":
            prtasks[i] = prtasks[i].apply(str)


    table = Table(title="TASKS", show_lines=False, header_style=theme, border_style="black", title_style=theme)
    columns = ["I", "CODES", "TYPE", "NAME", "CLASS", "DATE"]
    #gTaskCols = ["DATUM", "ART", "NAME", "UNTERRICHT", "CODE"]
    #columns = ["I", "CODES", "ART", "NAME", "UNTERRICHT", "DATUM"]
    #style = "green"

    for i in range(len(columns)):
        table.add_column(f"{columns[i]}", style = theme)
    for i in range(len(prtasks.index)):
        date = prtasks.iloc(axis=0)[i]["DATE"]
        if len(str(date.day)) < 2:
            prdate = "0" + str(date.day) + "/"
        else:
            prdate = str(date.day) + "/"
        if len(str(date.month)) < 2:
            prdate = prdate + "0" + str(date.month)
        else:
            prdate = prdate + str(date.month)
        if len(prtasks.iloc(axis=0)[i]["CODES"]) > 0:
            table.add_row(str(i), prtasks.iloc(axis=0)[i]["CODES"], prtasks.iloc(axis=0)[i]["TYPE"], prtasks.iloc(axis=0)[i]["NAME"], prtasks.iloc(axis=0)[i]["CLASS"], prdate)
        else:
            table.add_row(str(i), "X", prtasks.iloc(axis=0)[i]["TYPE"], prtasks.iloc(axis=0)[i]["NAME"], prtasks.iloc(axis=0)[i]["CLASS"], prdate)            
    console.print(table)
    print()
    
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
        if "A" in args.keys():
            aCode = args["A"]
        else:
            aCode = ""
    except Exception as e:
        console.print_exception()
        error = "ERROR: ADDITION FAILED"
        logger.error(e)


    apnd = [aDate, aType, aName, aClass, aCode]
    tasks.loc[len(tasks.index)] = apnd 
    #print(tasks)
   

"""def getInfo(args):
    ind = args["I"]
    info = args["F"]
    print(tasks.iloc(axis = 0)[ind][info])"""


def main():
    global running
    running = True
    global command
    initializer()
    while (running):
        tasks["DATE"] = pd.to_datetime(tasks["DATE"], format="%d/%m/%y").dt.strftime("%d/%m/%y")
        tasks.sort_values(by="DATE", ignore_index=True, inplace=True)
        if command != "LONG":
            printList()
        #uIn = input(">>")
        console.print("(TO-DO) >> ",style = theme, end="")
        uIn = input()
        uIn = uIn.upper()
        if "-" in uIn:
            hold = uIn.split("-")
            command = hold[0]
            command = command[:len(command)-1]
            #print("[" + command + "]")
        else:
            command = uIn
        if command in functs.values():
            call = [k for k, v in functs.items() if v == command][0]
            args = paramSplit(uIn)
            if len(args) == 0:
                if call == exit:
                    landing()
                    exit()
                else:
                    call()
            else:
                call(args)
        else:
            console.print("ERROR: UNRECOGNIZED COMMAND", style = alert)

main()
