import os, datetime, re, os, sys, platform
def ReadDataFromFile(strPath, strFileType):
    strComment = "#"
    try:
        objFile = open(strPath,"r")
        vList = []
        for strItem in objFile:
            strPattern = "(^[ \t]*(?:" + strComment + ")+.*$)|(^[ \t]+$)|(^$)"
            # Skip comment lines.
            if not re.search(strPattern, strItem):
                # Replace newline character that is included when reading a line
                strItem = strItem.replace("\n", "")
                vList.append(strItem)
        objFile.close
        return vList
    # SecureCRT on Mac uses Python 2.5, so use old syntax.
    # Python 2.7 syntax:
    # except Exception as strError:
    except Exception, strError:
        MsgBox("Could not open " + strFileType + " file with error: " + 
            str(strError))
        return 0
def Main():
    errorMessages = ""
    g_strPath = "/Users/lvcuong/PycharmProjects/JNPR/CRT"
    vHostsList = ReadDataFromFile(g_strPath + '/hosts.txt', "host")
    if not vHostsList:
        return
    vCommandsList = ReadDataFromFile(g_strPath + '/commands.txt', "commands")
    if not vCommandsList:
        return
    vUserandPassword = ReadDataFromFile(g_strPath + '/users.txt', "users")
    if not vUserandPassword:
        return
    for session in vHostsList:
        try:
            crt.Session.Connect("/TELNET " + session + " 23")
        except ScriptError:
            error = crt.GetLastErrorMessage()
        if crt.Session.Connected:
            crt.Screen.Synchronous = True
            crt.Screen.WaitForString("login:")
            crt.Screen.Send(vUserandPassword[0] + "\r")
            crt.Screen.WaitForString("Password:")
            crt.Screen.Send(vUserandPassword[1] + "\r")
            while True:	
                if crt.Screen.WaitForString(">"):
                    break
            row = crt.Screen.CurrentRow
            prompt = ">"
            check = crt.Screen.Get(row,0,row,7 )
            readline = crt.Screen.Get(row, 0,row,crt.Screen.CurrentColumn -2)
            crt.Session.Log(False)
            crt.Session.LogFileName = (g_strPath + "/%D-%M-%Y/" + readline + ".txt")
            crt.Session.Log(True,False,True)
            crt.Screen.Send("\r")
            crt.Screen.WaitForString(prompt,0)
            for cmd in vCommandsList:
                crt.Screen.Send(cmd + " |no-more \n")
                crt.Screen.WaitForString(prompt,0)
            crt.Session.Disconnect()
            while crt.Session.Connected == True:
                crt.Sleep(100)
            crt.Sleep(500)
        else:
            errorMessages = errorMessages + "\n" + "*** Error connecting to " + session + ": " + error
            crt.Session.Log(False)
            logfile = g_strPath + "/%H-error.log"
            crt.Session.LogFileName = logfile
            crt.Session.Log(True,False,True)
    crt.Quit()
Main()
