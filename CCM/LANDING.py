import os
import numpy as np
import pandas as pd
import asyncio
import datetime as dt
from CCM_Subroutines import *
import subprocess
import pathlib
import curses as c
from curses import wrapper
from rich.console import Console
#from playsound import playsound

console = Console()

file = os.path.basename(__file__)
path = pathlib.Path(__file__).parent.resolve()
os.chdir(path)
user = os.getlogin()


def To_Do():
    subprocess.run(["Python", f'{path}\To_Do.py'])
    exit()


def initializer():
    os.system("cls")
    global tasks
    tasks = initTasks()
    global taskN
    global path


    global command
    command = "INIT"
    #console.print("WELCOME, RED", style= theme)

    today = dt.date.today()
    tskLim = tasks.mask(tasks["DATE"] > (today + dt.timedelta(days = 7)))
    taskN = str(len(tskLim.index))

    global notifN
    notifN = [taskN]


def main(stdscr):
    c.cbreak(True)
    global xmax
    global ymax
    c.curs_set(0)
    #c.init_color()
    global htxt
    global hbk
    c.init_pair(1, int(htxt), int(hbk))
    home = c.color_pair(1)

    global amb
    amb = fr"{path}\amb.wav"
    #playsound(amb)
    ymax,xmax = stdscr.getmaxyx()
    
    #row, column
    stdscr.nodelay(True)

    global now
    tm = c.newwin(1, 25, round((5/44)*ymax), round((92/158)*xmax))
    tm.nodelay(True)
    now = dt.datetime.now().strftime("%H:%M:%S %Y-%m-%d")
    tm.erase()
    t = "[" + str(now) + "]" 
    tm.addstr(t, home)
    tm.refresh()


    notifs = c.newwin(30, 36, round((7/44)*ymax), round((45/158)*xmax))
    notifs.erase()
    j = 0
    notifs.addstr(j, 0, f"[{taskN}] TASKS DUE IN THE NEXT 7 DAYS", home)
    j += 4
    notifs.addstr(j, 0, "THIS IS A BETA VERSION OF THE CENTRAL COMMAND MODULE (CCM). PLEASE REPORT ANY AND ALL MODULE INSTABILITY TO THE RELEVANT DEVELOPERS.", home)
    j += 7
    notifs.addstr(j, 0, fr"PELASE REFER TO THE CCM USER MANUAL FOR FULL DOCUMENTATION, LOCATED AT {path}\DOCUMENTATION.TXT", home)
    notifs.refresh()
    printed = [taskN]

    cal = c.newwin(30, 30, round((7/44)*ymax), round((83/158)*xmax))
    #cal.nodelay(True)
    cal.erase()

    try:
        for i in events:
            print(i)
    except:
        cal.addstr("OUTLOOK INTEGRATION IS CURRENTLY DISABLED. TO ENABLE OUTLOOK INTEGRATION AND DISPLAY OUTLOOK CALENDER EVENTS, REFER TO CCM DOCUMENTATION.", home)
        #https://pietrowicz-eric.medium.com/how-to-read-microsoft-outlook-calendars-with-python-bdf257132318
    cal.refresh()


    CCMvw = c.newwin(1, 20, round((5/44)*ymax), round((74/158)*xmax))
    CCMvw.erase()
    CCMvw.addstr(CCMv, home)
    CCMvw.refresh()

    global uname
    global ushow
    login = c.newwin(1, 20, round((5/44)*ymax), round((45/158)*xmax))
    login.erase()
    uname = user.upper()
    ushow = uname
    #login.addstr(f"USER: {uname}")
    login.addstr(f"USER: {uname}", home)
    login.refresh()

    iarrow = c.newwin(1, 42, round((40/44)*ymax), round((45/158)*xmax))
    iarrow.nodelay(True)
    iarrow.clear()
    iarrow.addstr("(HOME) >> PRESS ANY KEY TO ENTER CLI MODE", home)
    iarrow.refresh()

    go = True
    while go:

        try:
            key = iarrow.getkey()
        except:
            key = ""

        if now != dt.datetime.now().strftime("%H:%M:%S %Y-%m-%d"):
            tm.erase()
            now = dt.datetime.now().strftime("%H:%M:%S %Y-%m-%d")
            t = "[" + str(now) + "]" 
            tm.addstr(t, home)
            tm.refresh()

        if ushow != uname:
            login.erase()
            ushow = uname
            login.addstr(f"USER: {uname}", home)
            login.refresh()
        
        #notifRefresh()

        if notifN != printed:
            notifs.erase()
            j = 0
            notifs.addstr(j, 0, f"[{taskN}] TASKS DUE IN THE NEXT 7 DAYS", home)
            j += 4
            notifs.addstr(j, 0, "THIS IS A BETA VERSION OF THE CENTRAL COMMAND MODULE (CCM). PLEASE REPORT ANY AND ALL MODULE INSTABILITY TO THE RELEVANT DEVELOPERS.", home)
            j += 7
            notifs.addstr(j, 0, fr"PELASE REFER TO THE CCM USER MANUAL FOR FULL DOCUMENTATION, LOCATED AT {path}\DOCUMENTATION.TXT", home)
            notifs.refresh()
            printed = [taskN]


        if len(key) > 0:
            go = False
            #playsound(fr"{path}\beep.mp3")

    c.endwin()
        

initializer()

wrapper(main)

try:
    saveTasks(tasks)
except Exception as e:
    logger.error(e)

subprocess.run(["Python", fr'{path}\CLI.py'])
exit()

