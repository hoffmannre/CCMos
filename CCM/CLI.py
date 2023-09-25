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
from pynput.keyboard import Key, Controller
import configupdater
#from To_Do import *

keyboard = Controller()
updater = ConfigUpdater()



import warnings
warnings.filterwarnings("ignore")


def initializer():
    os.system("cls")
    keyboard.tap(Key.esc)
    console.print("INITIALIZING TASK DATAFRAME...",style = theme, sep = " ", highlight=False, end = "")
    global tasks
    tasks = initTasks()
    console.print("SUCCESS!", style = theme)
    
    console.print("INIZIALIZING USER VARIABLES...",style = theme, sep = " ", highlight=False, end = "")
    global user, path
    user, path = getUserPath()
    user = user.upper()
    console.print("SUCCESS!", style = theme)
    print()
    
    global functs
    functs = {
         exit : "EXIT",
         moveto : "ACCESS",
         landing : "HOME",
         settings : "CONFIG",
         printList : "TODO",
    }
    global command
    command = "INIT"

    console.print(CCMv, style = theme, highlight=False)
    console.print("USER: " + os.getlogin().upper(), style = theme)
    print()
    print()
    console.print("WELCOME, " + user, style = theme)
    print()
    print()
    print()
    print()
    print()
    print()


def printList(args = ""):
    global command
    """if command != "INIT":
        os.system("cls")
        print()"""

    global today

    if len(args) > 1:
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
    else:
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

def settings(args = ""):
    print()
    print()
    updater.read(fr"{path}\config.ini")
    try:
        if len(args) > 1:
            console.print("PLEASE RETURN TO HOME AND RE-ENTER CLI MODE TO SEE STYLE, ALERT, OR USER CHANGES", style = alert)
            print()
            if (args["N"] == "STYLE") or (args["N"] == "ALERT"):
                updater[args["S"]][args["N"].lower()].value = args["V"].lower()
                updater.update_file()
                configParse()
            else:
                updater[args["S"]][args["N"].lower()].value = args["V"]
                updater.update_file()
                configParse()
    except Exception as e:
        logger.log(e)
        #console.print("ERROR: INVALID INPUT. NOTE THAT CONFIG VALUES ARE CASE SENSITIVE AND ALL COLORS MUST BE LOWER CASE.", style = alert)
    table = Table(title="SETTINGS", show_lines=False, header_style=theme, border_style="black", title_style=theme)
    cols = ["SECTION", "NAME", "VALUE"]
    for i in cols:
        table.add_column(i)
    for i in config:
        for j in config[i]:
            table.add_row(i, j, config[i][j], style=theme)
    
    console.print(table)
    print()



def main():
    global running
    running = True
    global command
    initializer()
    while (running): 
        console.print("(BASE) >> ",style = theme, end="")
        uIn = input()
        uIn = uIn.upper()
        if "-" in uIn:
            hold = uIn.split("-")
            command = hold[0]
            command = command[:len(command)-1]
        else:
            command = uIn
        try:
            if command in functs.values():
                call = [k for k, v in functs.items() if v == command][0]
                args = paramSplit(uIn)
                if len(args) == 0:
                    if call == exit:
                        exit()
                    else:
                        call()
                elif call == moveto:
                    call(args)
                    exit()
                else:
                    call(args)
            elif command == "":
                pass
            else:
                print()
                console.print("ERROR: UNRECOGNIZED COMMAND", style = alert, end="\n\n")
        except Exception as e:
            print()
            console.print("ERROR", style = alert,end="\n\n")
            logger.error(e)
main()