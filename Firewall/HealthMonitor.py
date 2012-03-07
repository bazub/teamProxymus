import subprocess
from tkinter.messagebox import *
from tkinter import *


root=Tk()
root.geometry("640x480+400+100")
root.title("HM HealthMonitor©                                                                    by Proxymus")
root.bind("<Escape>", lambda e: e.widget.quit())
root.resizable(FALSE,FALSE)
def PIcomm():
    a=subprocess.call("PING 10.140.16.47")
    if a:
        showwarning("ERROR!!","Your Apache server is down!")
    else:
        showwarning(" ","Your Apache serves is online!")

butPI=Button(root, text="Check Apache", command=PIcomm,width="20")
butPI.grid(row=0,column=1)
subprocess.call("scp root@10.140.16.47:/var/log/squid/access.log C:/access.log")

root.mainloop()    