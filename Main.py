import tkinter as tk
import pdb #Importing Debugger
import Initialization
import Funs
import time
import StyleFormat
from tkinter import ttk
from ttkthemes import themed_tk as tkth

def update_Var():
    global loopBool
    loopBool = False
    root.destroy()
    #if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
    #    root.destroy()

def SetMainWindow(master):
    #Set parametes for main window opening
    root.geometry("1750x900+50+50") #Main Window Placement
    root.title("Financial Helper") #Title of the Window
    root.iconbitmap(r"Icons\Icon.ico") #Icon of the Window
    root.config(bg = "white")
    Funs.SetGridWeight(3, 2, root, [0,1],[0])
    
if __name__ == "__main__":
    loopBool = True
    newWindowBG = 'PaleTurquoise1'#'PaleTurquoise1'#'PaleGreen1'#'OliveDrab1'#'coral'#'LightGoldenrod1'#'light sky blue'
    #root = tk.Tk()
    root = tkth.ThemedTk()
    starttime=time.time()
    root.protocol("WM_DELETE_WINDOW", update_Var)

    #MAIN CODE ------------------------------------------------------
    SetMainWindow(root)

    mainWindow = Initialization.MainWindow(root)
    
    #END CODE--------------------------------------------------------

    #root.mainloop()
    while loopBool:
        autoSaveTime = 60 #Time to autosave in seconds
        currTime = time.time()
        timePassed = currTime - starttime
        clk = list(time.localtime())
        if timePassed > autoSaveTime:
            starttime = currTime
            Funs.saveData(mainWindow.allAcc)
            #timeStamp = DD/MM/YYYY at HH:MM
            if len(str(clk[4])) == 1:
                timeStamp = str(clk[2]) + "/" + str(clk[1]) + "/" +  str(clk[0]) + " at " + str(clk[3]) + ":0" + str(clk[4])
            else:
                timeStamp = str(clk[2]) + "/" + str(clk[1]) + "/" +  str(clk[0]) + " at " + str(clk[3]) + ":" + str(clk[4])
            mainWindow.statusBar.Update("Saved -- " + timeStamp)
        root.update_idletasks()
        root.update()

        time.sleep(0.01)
