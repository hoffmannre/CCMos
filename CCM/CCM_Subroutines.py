import numpy as np
import pandas as pd
import asyncio
import datetime as dt
import os
import subprocess
import logging
import warnings
import pathlib
import configparser
import curses as c
from configupdater import ConfigUpdater

config = configparser.ConfigParser()


file = os.path.basename(__file__)
path = pathlib.Path(__file__).parent.resolve()
os.chdir(path)
#user = os.getlogin()
#user = "RED"
CCMv = "CCM v0.2.0"
config.read(fr"{path}\config.ini")



from rich.console import Console


console = Console()
theme = "red"
alert = "bold dark_red"

targets = ["TO DO", "HOME"]



def configParse():
    config.read(fr"{path}\config.ini")
    global htxt, hbk, user, theme, List_Time, alert
    htxt = config['HOME']['HOMETXT']
    hbk = config['HOME']['HOMEBACK']

    if config['GLOBAL']['USER'] == "?" or config['GLOBAL']['USER'] == "":
        config.set("GLOBAL", "USER", os.getlogin())
    user = config['GLOBAL']['USER']

    List_Time = config['TO_DO']['LIST_TIME']
    theme = config['CLI']['STYLE']
    alert = config['CLI']['ALERT']


#console.print("DATAFRAME CONSTRUCTED", style= theme)
try:
    logging.basicConfig(filename=r'\logs\CCM.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')
except FileNotFoundError:
    os.mkdir(r'\logs')
    open(fr'C:\Users\{user}\Documents\VScode\CCM\logs\CCM.log', "w")
    logging.basicConfig(filename=r'\logs\CCM.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(message)s')

logger=logging.getLogger(__name__)

warnings.filterwarnings("ignore")



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




"""def editConfig(args):
    section = args["S"]
    key = args["K"]
    value = args["V"]
    config.set(section, key, value)
    #console.print("ALERT: ALL CHAGES WILL BE UNDONE ON CLOSING THE PROGRAM. EDIT THE CONFIGURATION FILE 'CONFIG.INI' TO PERMANENTLY CHANGE VALUES", style = alert)
"""



def getUserPath():
      global user
      global path
      return(user,path)

def initTasks():
    global today
    global tasks
    global taskCols

    taskCols = [ "DATE", "TYPE", "NAME", "CLASS", "CODES"]
    today = dt.date.today()

    try:
        tasks = pd.read_parquet(r'ToDo_List.parquet')
        tasks = tasks[tasks.columns.intersection(taskCols)]
    except Exception as e:
        tasks = pd.DataFrame(columns = taskCols)
    tasks["DATE"] = pd.to_datetime(tasks["DATE"], dayfirst=True, format="%d/%m/%y", errors = "raise").dt.date
    tasks = tasks.reindex(columns=taskCols, fill_value="")

    for i in tasks.index:
        if (tasks.iloc[i]["DATE"] < today) and ("!" not in tasks.iloc[i]["CODES"]):
            if len(tasks.iloc[i]["CODES"]) == 0:
                tasks.iloc[i]["CODES"] = tasks.iloc[i]["CODES"] + "!"
            else:
                tasks.iloc[i]["CODES"] = tasks.iloc[i]["CODES"] + ", !"
    #console.print("DATAFRAME CONSTRUCTED", style= theme)

    return(tasks)

def saveTasks(df):
    df.to_parquet(path=r'ToDo_List.parquet')
    console.print("DATAFRAME SAVED", style= theme)
    
def landing():
    print()
    try:
        saveTasks(tasks)
    except Exception as e:
        logger.error(e)

    subprocess.run(["Python", fr'{path}\LANDING.py'])

def moveto(args):
    #print()
    try:
        saveTasks(tasks)
    except Exception as e:
        logger.error(e)

    target = args["T"]
    
    try:
        if target == "TO DO" or target == "TODO":
            subprocess.run(["Python", fr'{path}\To_Do.py']) 
        if target == "HOME":
            subprocess.run(["Python", fr'{path}\LANDING.py'])
        """else:
            console.print("INVALED ACCESS TARGET. AVAILABLE TARGETS:", style = theme)
            for i in (targets):
                sel = "    -T " + i
                console.print(sel, style = theme)"""
    except:
        pass

def scaleX(int, max):
    scaled = round((int/158)*max)
    print(scaled)
    return scaled

def scaleY(int, max):
    scaled = round((int/44)*max)
    return scaled


configParse()