"""def initializer():
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
    tasks.sort_values(by="DATE", ignore_index=True, inplace=True)
    print("DATAFRAMES CONSTRUCTED")
    print()
    global functs
    functs = {
        To_Do : "TODO",
        exit : "EXIT"
    }
    print("WELCOME, RED")"""

    while True:
        if now != time.localtime():
            tm.erase()
            now = time.localtime()
            ctime = time.strftime("%H:%M:%S", now)
            t = "[" + str(ctime) + "]" 
            tm.addstr(t, red)
            tm.refresh()
        else:
            tm.erase()
            tm.addstr(t, red)
            tm.refresh()
            

        if today != dt.date.today():
            day.erase()
            today = dt.date.today()
            d = "[" + str(today) + "]" 
            day.addstr(d, red)
            day.refresh()
        else:
            day.erase()
            day.addstr(d, red)
            day.refresh()